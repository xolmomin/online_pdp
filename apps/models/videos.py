from django.core.validators import FileExtensionValidator
from django.db.models import TextChoices, ImageField, FileField, ForeignKey, CASCADE
from django.db.models.fields import CharField, TextField

from apps.models import UUIDBaseModel, CreatedBaseModel


class Video(UUIDBaseModel, CreatedBaseModel):
    class Status(TextChoices):
        READY = 'ready', 'Ready'
        PROCESSING = 'processing', 'Processing'
        FAILED = 'failed', 'Failed'

    title = CharField(max_length=255)
    status = CharField(max_length=255, choices=Status.choices, default=Status.PROCESSING)
    description = TextField()
    tags = CharField(max_length=255)
    image = ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    subtitle_lang = CharField(max_length=255)
    subtitle_file = FileField(upload_to='subtitle/%Y/%m/%d')
    created_by = ForeignKey('users.User', CASCADE)