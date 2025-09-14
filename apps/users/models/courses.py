from django.db.models import TextChoices, ForeignKey, CASCADE, ManyToManyField, URLField, FileField
from django.db.models.fields import CharField, IntegerField, BooleanField, DecimalField
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel, OrderBaseModel


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
    full_description = CKEditor5Field()
    short_description = CKEditor5Field()
    has_certificate = BooleanField(db_default=True)
    has_support = BooleanField()
    practice_count = IntegerField()
    valid_days = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)
    rating = DecimalField(max_digits=3, decimal_places=1)
    video_count = IntegerField()
    video_duration = IntegerField()
    topic = ForeignKey('users.Topic', CASCADE)

    teachers = ManyToManyField('users.User', blank=True)

    # class Meta:
    #     verbose_name = 'Kurs'
    #     verbose_name_plural = 'Kurslar'


class Section(CreatedBaseModel, OrderBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    course = ForeignKey('users.Course', CASCADE)


class Lesson(CreatedBaseModel, OrderBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    class AccessType(TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    access_type = CharField(max_length=20, choices=AccessType.choices, default=AccessType.PRIVATE)
    video_duration = IntegerField()
    section = ForeignKey('users.Section', CASCADE)
    video_link = URLField()
    video = FileField(upload_to='videos/')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        print(123)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    # content = ?
