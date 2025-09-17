from django.db.models import CharField, ForeignKey, CASCADE
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel


class SectionInterview(CreatedBaseModel):
    title = CharField(max_length=255)
    full_description = CKEditor5Field()
    short_description = CKEditor5Field()


class Part(CreatedBaseModel):
    title = CharField(max_length=255)
    question = CKEditor5Field()
    answer = CKEditor5Field()
    asked_by = CharField(max_length=50, null=True, blank=True)
    section_interview = ForeignKey('users.SectionInterview', CASCADE)
