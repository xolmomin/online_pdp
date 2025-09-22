from django.db.models import CharField, ForeignKey, CASCADE
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import CreatedBaseModel


class Interview(CreatedBaseModel):
    title = CharField(max_length=255)
    description = CKEditor5Field()


class InterviewPart(CreatedBaseModel):
    question = CKEditor5Field()
    answer = CKEditor5Field()
    interview = ForeignKey('users.Interview', CASCADE, related_name='parts')
