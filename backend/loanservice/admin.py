from django.contrib import admin

from .models import Applicant, LoanRequest

class LoanRequestAdmin(admin.ModelAdmin):
    list_display = (
                    'applicant_name',
                    'amount',
                    'approved',
                    'slug',
                    )
    search_fields = (
                    'amount',
                    'approved',
                    'slug',
                    'applicant__first_name',
                    'applicant__last_name',
                    'applicant__dni',
                    'applicant__gender',
                    )
    ordering = (
                'approved',
                'amount',
                'applicant__gender',
                'applicant__last_name',
                'applicant__first_name',
                'applicant__dni',
                'slug',
                )
    list_filter = (
                    'amount',
                    'approved',
                    'applicant__last_name',
                    'applicant__gender',
                    )

    
    def applicant_name(self, obj):
        return f"{obj.applicant.pk} - {obj.applicant.first_name} {obj.applicant.last_name}"

    applicant_name.short_description = "Pk - Applicant"

class LoanRequestInline(admin.TabularInline):
    model = LoanRequest
    extra = 3

class ApplicantAdmin(admin.ModelAdmin):
    list_display = (
                    'dni',
                    'last_name',
                    'first_name',
                    'email',
                    'gender',
                    'slug',
                    )
    search_fields = (
                    'dni',
                    'last_name',
                    'first_name',
                    'email',
                    'gender',
                    'slug',
                    )
    ordering = (
                'gender',
                'last_name',
                'first_name',
                'dni',
                'slug',
                )
    list_filter = (
                    'dni',
                    'last_name',
                    'first_name',
                    'gender',
                    )
    inlines = (
                LoanRequestInline,
                )

# Register your models here.
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)