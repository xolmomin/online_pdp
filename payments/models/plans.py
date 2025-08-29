from django.db.models import TextChoices
from django.db.models.fields import CharField, DecimalField, IntegerField

from payments.models import UUIDBaseModel, CreatedBaseModel


class Plan(UUIDBaseModel, CreatedBaseModel):
    class Status(TextChoices):
        ANNUAL = 'annual', 'Annual'
        MONTH = 'month', 'Month'

    title = CharField(max_length=255)
    bandwidth = CharField(max_length=255)
    storage = CharField(max_length=255)
    amount = DecimalField(max_digits=10, decimal_places=2)
    validity = IntegerField()