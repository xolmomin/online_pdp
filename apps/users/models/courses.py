from django.db.models import TextChoices, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, TextField, IntegerField, BooleanField, DecimalField

from apps.shared.models import UUIDBaseModel, CreatedBaseModel


class Topic(UUIDBaseModel):
    name = CharField(max_length=255)
    course = ForeignKey('users.Course', CASCADE)

class Course(UUIDBaseModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        ELEMENTARY = 'elementary', 'Elementary'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCE = 'advance', 'Advance'

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    description = TextField()
    has_certificate = BooleanField(db_default=True)
    has_support = BooleanField()
    practice_count = IntegerField()
    valid_days = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)
    rating = IntegerField()
    video_count = IntegerField()
    video_duration = IntegerField()
    teachers = ManyToManyField('users.User', blank=True)
    section = ForeignKey('users.Section', CASCADE)


class Section(UUIDBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'

    name = CharField(max_length=255)
    order_number = IntegerField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    lesson = ForeignKey('users.Lesson', CASCADE)

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

