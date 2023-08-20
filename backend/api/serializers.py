from rest_framework import serializers
from loanservice.models import Applicant, LoanRequest

class LoanRequestSerializer(serializers.HyperlinkedModelSerializer):
    """
        Loan Request serializer class
    """

    class Meta:
        model = LoanRequest
        fields = ['url', 'amount', 'applicant', 'approved']
        read_only_fields = ['approved']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'applicant': {'lookup_field': 'slug'},
        }

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    """
        Applicant serializer class
    """

    loanrequests = LoanRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Applicant
        fields = ['url', 'dni', 'first_name', 'last_name', 'gender', 'email', 'loanrequests']
        depth = 1
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


