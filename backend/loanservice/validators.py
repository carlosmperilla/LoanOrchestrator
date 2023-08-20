from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class NumericValidator:
    def __init__(self, message=None):
        if not message:
            message = _("%(value)s is not a numeric value")
        self.message = message

    def __call__(self, value):
        if not value.isnumeric():
            raise ValidationError(self.message, params={"value": value})

    def __eq__(self, other):
        return isinstance(other, NumericValidator) and self.message == other.message

    def deconstruct(self):
        path = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        args = ()
        kwargs = {"message": self.message}
        return path, args, kwargs
