import uuid

from django.db.models import Model, Func
from django.db.models.fields import DateTimeField, UUIDField, IntegerField, CharField, SlugField
from django.utils.text import slugify


class GenRandomUUID(Func):
    """
    Represents the PostgreSQL gen_random_uuid() function.
    """
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), default=uuid.uuid4(), editable=False)

    class Meta:
        abstract = True
        required_db_vendor = 'postgresql'


class CreatedBaseModel(UUIDBaseModel):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class OrderBaseModel(Model):
    order_number = IntegerField(db_default=0)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    slug = SlugField(unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
