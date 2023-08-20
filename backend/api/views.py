import requests
import random

from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_control

from loanservice.models import Applicant, LoanRequest

from rest_framework import viewsets, filters

from .serializers import ApplicantSerializer, LoanRequestSerializer

from .custom_permissions import AdminOrPostOnlyPermission

from .handle_custom_filters.custom_filters import (
    ByApplicantAttrFilterBackend,
    ByLoanRequestAttrFilterBackend,
    ByAmountRangeFilterBackend,
)
from .custom_schemas.applicant_schemas import (
    applicant_list_schema,
    applicant_retrieve_schema,
    applicant_create_schema,
    applicant_update_schema,
    applicant_partial_update_schema,
    applicant_destroy_schema,
)
from .custom_schemas.loanrequest_schemas import (
    loanrequest_list_schema,
    loanrequest_retrieve_schema,
    loanrequest_create_schema,
    loanrequest_update_schema,
    loanrequest_partial_update_schema,
    loanrequest_destroy_schema,
)

from celery import shared_task


@shared_task
def invalidate_cache(cache_keys):
    cache.delete_many(cache_keys)


@method_decorator(name="list", decorator=applicant_list_schema)
@method_decorator(name="retrieve", decorator=applicant_retrieve_schema)
@method_decorator(name="create", decorator=applicant_create_schema)
@method_decorator(name="update", decorator=applicant_update_schema)
@method_decorator(name="partial_update", decorator=applicant_partial_update_schema)
@method_decorator(name="destroy", decorator=applicant_destroy_schema)
@method_decorator(name="list", decorator=cache_control(must_revalidate=True))
class ApplicantViewSet(viewsets.ModelViewSet):
    """
    Esta vista permite **ver, crear, modificar y eliminar Applicants**.
    ## <span style="color:darkslateblue">Filtros</span>

    Puede usar get-parameters para **filtrar por atributo**, por ejemplo.

    > api/applicants/?attr_name=value
    """

    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [AdminOrPostOnlyPermission]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        ByApplicantAttrFilterBackend,
    ]
    search_fields = ["first_name", "last_name", "dni"]
    ordering_fields = ["gender", "first_name", "last_name", "dni"]
    ordering = ["gender", "first_name", "last_name"]
    lookup_field = "slug"

    def initial(self, request, *args, **kwargs):
        self.cache_key = f"Applicants_cache_{self.request.user.pk}"
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        cache_queryset = cache.get(self.cache_key)
        if cache_queryset is None:
            cache_queryset = self.queryset
            cache.set(
                self.cache_key, cache_queryset, 60 * 60 * 2
            )  # expires in 2h at the latest
        return cache_queryset

    def perform_create(self, serializer):
        invalidate_cache.delay([self.cache_key])
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        invalidate_cache.delay([self.cache_key])
        serializer.save()

    def perform_destroy(self, instance):
        invalidate_cache.delay([self.cache_key])
        return super().perform_destroy(instance)


@method_decorator(name="list", decorator=loanrequest_list_schema)
@method_decorator(name="retrieve", decorator=loanrequest_retrieve_schema)
@method_decorator(name="create", decorator=loanrequest_create_schema)
@method_decorator(name="update", decorator=loanrequest_update_schema)
@method_decorator(name="partial_update", decorator=loanrequest_partial_update_schema)
@method_decorator(name="destroy", decorator=loanrequest_destroy_schema)
@method_decorator(name="list", decorator=cache_control(must_revalidate=True))
class LoanRequestViewSet(viewsets.ModelViewSet):
    """
    Esta vista permite **ver, crear, modificar y eliminar LoanRequestos**.
    ## <span style="color:darkslateblue">Filtros</span>

    Puede usar get-parameters para **filtrar por atributo**, por ejemplo.

    > api/loanrequests/?attr_name=value

    Tambien por **rango**, con *min_amount* y *max_amount* o con *min_amount* y *max_amount*.
    > api/loanrequests/?min_amount=1200.5&max_amount=80000

    > api/loanrequests/?min_amount=50.2

    > api/loanrequests/?max_amount=700.45
    """

    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [AdminOrPostOnlyPermission]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        ByLoanRequestAttrFilterBackend,
        ByAmountRangeFilterBackend,
    ]
    search_fields = ["approved", "amount"]
    ordering_fields = ["amount", "approved"]
    ordering = ["approved", "-amount"]
    lookup_field = "slug"

    def initial(self, request, *args, **kwargs):
        self.cache_key = f"LoanRequests_cache_{self.request.user.pk}"
        self.cache_keys = [
            f"LoanRequests_cache_{self.request.user.pk}",
            f"Applicants_cache_{self.request.user.pk}",
        ]
        return super().initial(request, *args, **kwargs)

    def is_approved(self, serializer):
        return random.choice([False, True])

    def get_queryset(self):
        cache_queryset = cache.get(self.cache_key)
        if cache_queryset is None:
            cache_queryset = self.queryset
            cache.set(
                self.cache_key, cache_queryset, 60 * 60 * 2
            )  # expires in 2h at the latest

        return cache_queryset

    def perform_create(self, serializer):
        invalidate_cache.delay(self.cache_keys)
        approved = self.is_approved(serializer)
        serializer.save(approved=approved)

    def perform_update(self, serializer):
        invalidate_cache.delay(self.cache_keys)
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        invalidate_cache.delay(self.cache_keys)
        return super().perform_destroy(instance)
