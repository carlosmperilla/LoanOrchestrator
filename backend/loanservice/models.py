import uuid

from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)
from django.utils.translation import gettext_lazy as _
from .validators import NumericValidator


class Applicant(models.Model):
    GENDER_CHOICES = [
        ("M", _("Masculino")),
        ("F", _("Femenino")),
        ("O", _("Otro")),
    ]
    slug = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="Identificador único de Solicitante de prestamo",
    )
    dni = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=8,
        verbose_name="DNI",
        validators=[
            MinLengthValidator(8),
            NumericValidator(_("%(value)s no es un valor númerico")),
        ],
    )
    first_name = models.CharField(
        null=False, blank=False, max_length=50, verbose_name="Nombre"
    )
    last_name = models.CharField(
        null=False, blank=False, max_length=50, verbose_name="Apellido"
    )
    gender = models.CharField(
        null=False,
        blank=False,
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Género",
    )
    email = models.EmailField(
        null=False, blank=False, unique=True, verbose_name="e-mail"
    )

    class Meta:
        verbose_name = "Solicitante"
        verbose_name_plural = "Solicitantes"
        ordering = ["gender", "last_name", "first_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class LoanRequest(models.Model):
    slug = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="Identificador único de Petición de prestamo",
    )
    amount = models.DecimalField(
        default=0.0,
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto solicitado",
        validators=[MinValueValidator(0.0), MaxValueValidator(9999999999)],
    )
    approved = models.BooleanField(default=False, verbose_name="¿Está aprobado?")
    applicant = models.ForeignKey(
        Applicant,
        editable=True,
        on_delete=models.CASCADE,
        related_name="loanrequests",
        verbose_name="Solicitante",
    )

    class Meta:
        verbose_name = "Petición de prestamo"
        verbose_name_plural = "Peticiones de prestamo"
        ordering = ["approved", "-amount"]

    def __str__(self):
        return str(self.applicant) + " - " + str(self.amount)
