from django.core.validators import FileExtensionValidator
from django.db.models import TextChoices, ForeignKey, CASCADE, ManyToManyField, URLField, FileField, SET_NULL, \
    CheckConstraint, Q
from django.db.models.fields import CharField, IntegerField, BooleanField, SmallIntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel, OrderBaseModel


class Category(CreatedBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(CreatedBaseModel):
    class Level(TextChoices):
        BEGINNER = 'beginner', _('Beginner')
        ELEMENTARY = 'elementary', _('Elementary')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')

    name = CharField(max_length=255)
    level = CharField(max_length=20, choices=Level.choices)
    full_description = CKEditor5Field()
    short_description = CKEditor5Field(blank=True)
    has_certificate = BooleanField(default=True, db_default=True)
    has_support = BooleanField(default=False, db_default=False)
    practice_count = IntegerField(default=0, db_default=0, editable=False)
    valid_days = IntegerField()
    price = IntegerField()
    rating = SmallIntegerField(default=50, editable=False)
    video_count = IntegerField(default=0, db_default=0, editable=False)
    total_video_duration = IntegerField(default=0, db_default=0, editable=False)
    category = ForeignKey('users.Category', SET_NULL, null=True, blank=True)
    teachers = ManyToManyField('users.User', blank=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=50),
                name='rating_check_constraints'
            ),
        ]

    def __str__(self):
        return self.name


class Section(CreatedBaseModel, OrderBaseModel):
    class Status(TextChoices):
        PUBLISHED = 'published', 'Published'
        UNPUBLISHED = 'unpublished', 'Unpublished'

    name = CharField(max_length=255)
    status = CharField(max_length=20, choices=Status.choices, default=Status.UNPUBLISHED)
    course = ForeignKey('users.Course', CASCADE)
    video_count = IntegerField(default=0, db_default=0, editable=False)
    total_video_duration = IntegerField(default=0, db_default=0, editable=False)

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
    video_duration = IntegerField(db_default=0, editable=False)
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
