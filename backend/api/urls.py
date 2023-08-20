from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views


router = routers.DefaultRouter()
router.register(r'applicants', views.ApplicantViewSet)
router.register(r'loanrequests', views.LoanRequestViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Loan Servie API v1",
      default_version='v1',
      description="API v1. Manage Loan Request data.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="carlosperillaprogramacion@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('authentication/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]