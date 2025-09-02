from django.db.models import TextChoices, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, TextField, IntegerField, BooleanField, DecimalField

from apps.shared.models import UUIDBaseModel, CreatedBaseModel


class Topic(CreatedBaseModel):
    name = CharField(max_length=255)


class Course(CreatedBaseModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        ELEMENTARY = 'elementary', 'Elementary'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    description = TextField()  # TODO ckeditor qoshish
    has_certificate = BooleanField(db_default=True)
    has_support = BooleanField()
    practice_count = IntegerField()
    valid_days = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)
    rating = IntegerField()
    video_count = IntegerField()
    video_duration = IntegerField()
    topic = ForeignKey('users.Topic', CASCADE)

    teachers = ManyToManyField('users.User', blank=True)


class Section(CreatedBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'

    name = CharField(max_length=255)
    order_number = IntegerField()  # TODO ordering_number OrderBase
    status = CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    course = ForeignKey('users.Course', CASCADE)


class Lesson(CreatedBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        # TODO UNPUBLISHED

    class AccessType(TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = CharField(max_length=255)
    order_number = IntegerField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    access_type = CharField(max_length=20, choices=AccessType.choices, default=AccessType.PRIVATE)
    video_duration = IntegerField()
    section = ForeignKey('users.Section', CASCADE)

    # video_link  TODO
