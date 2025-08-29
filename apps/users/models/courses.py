from django.core.validators import FileExtensionValidator
from django.db.models import TextChoices, ImageField, FileField, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, TextField, IntegerField, BooleanField

from apps.shared.models import UUIDBaseModel, CreatedBaseModel


class Course(UUIDBaseModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        ELEMENTARY = 'elementary', 'Elementary'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCE = 'advance', 'Advance'

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    has_certificate = BooleanField(db_default=True)
    valid_days = IntegerField()

    teachers = ManyToManyField('users.User')


class Topic(UUIDBaseModel):
    name = CharField(max_length=255)


class Section(UUIDBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'

    name = CharField(max_length=255)
    order_number = IntegerField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    # lesson =

class Lesson(UUIDBaseModel, CreatedBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'

    class AccessType(TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = CharField(max_length=255)
    order_number = IntegerField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    access_type = CharField(max_length=20, choices=AccessType.choices, default=AccessType.PRIVATE)
    video_duration = IntegerField()
    # video_link  TODO




# class Video(UUIDBaseModel, CreatedBaseModel):
#     class Status(TextChoices):
#         READY = 'ready', 'Ready'
#         PROCESSING = 'processing', 'Processing'
#         FAILED = 'failed', 'Failed'
#
#     title = CharField(max_length=255)
#     status = CharField(max_length=255, choices=Status.choices, default=Status.PROCESSING)
#     description = TextField()
#     tags = CharField(max_length=255)
#     image = ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True,
#                        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
#     subtitle_lang = CharField(max_length=255)
#     subtitle_file = FileField(upload_to='subtitle/%Y/%m/%d')
#     created_by = ForeignKey('users.User', CASCADE)
