from django.core.validators import FileExtensionValidator
from django.db.models import TextChoices, ForeignKey, CASCADE, ManyToManyField, URLField, FileField, SET_NULL, \
    CheckConstraint, Q
from django.db.models.fields import CharField, IntegerField, BooleanField, SmallIntegerField
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel, OrderBaseModel
from django.utils.translation import gettext_lazy as _

class Topic(CreatedBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(CreatedBaseModel):  # TODO Module
    class Level(TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        ELEMENTARY = 'elementary', 'Elementary'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    full_description = CKEditor5Field()
    short_description = CKEditor5Field()
    has_certificate = BooleanField(default=True, db_default=True)
    has_support = BooleanField(default=False, db_default=False)
    practice_count = IntegerField(default=0, db_default=0, editable=False)
    valid_days = IntegerField()
    price = IntegerField()
    rating = SmallIntegerField(editable=False, default=50)
    video_count = IntegerField(default=0, db_default=0, editable=False)
    video_duration = IntegerField(default=0, db_default=0, editable=False)
    topic = ForeignKey('users.Topic', SET_NULL, null=True, blank=True)
    teachers = ManyToManyField('users.User', blank=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=50),
                name='rating_check_constraints'
            ),
            # Add more CheckConstraint instances as needed
        ]

    def __str__(self):
        return self.name


class Section(CreatedBaseModel, OrderBaseModel):  # TODO lesson
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    course = ForeignKey('users.Course', CASCADE)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.name


class Lesson(CreatedBaseModel, OrderBaseModel):  # TODO Parts
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    class AccessType(TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    access_type = CharField(max_length=20, choices=AccessType.choices, default=AccessType.PRIVATE)
    video_duration = IntegerField(db_default=0)
    section = ForeignKey('users.Section', CASCADE)
    video_link = URLField()
    video = FileField(upload_to='videos/%Y/%m/%d',
                      help_text="video's format must be 'mp4', 'mov', 'webm'",
                      validators=[FileExtensionValidator(['mp4', 'mov', 'webm'])]
                      )

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    # content = ?
