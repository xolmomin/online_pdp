from django.db.models import ManyToManyField, ForeignKey, JSONField, CASCADE, Model
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DateTimeField
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import SlugBaseModel


class Topic(SlugBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def problem_count(self):
        return Problem.objects.filter(topics=self).count()


class Problem(Model):
    class Difficulty(TextChoices):
        EASY = 'Easy'
        MEDIUM = 'Medium'
        HARD = 'Hard'

    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    difficulty = CharField(max_length=15, choices=Difficulty.choices)
    topics = ManyToManyField('tasks.Topic', blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Example(Model):
    example = JSONField()
    task = ForeignKey('tasks.Problem', CASCADE, related_name='examples')
