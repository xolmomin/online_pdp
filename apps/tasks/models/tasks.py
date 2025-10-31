from django.db.models import ManyToManyField, ForeignKey, CASCADE, Model
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DateTimeField, TextField
from django_ckeditor_5.fields import CKEditor5Field

from shared.models import SlugBaseModel


# TODO - Profile - solved problems (Easy 10 / 100) (Leetcode), problems: success, in process, failed (robocontest.uz)
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

    class Meta:
        ordering = ['id']


class Example(Model):
    input = CharField(max_length=255)
    output = CharField(max_length=255)
    explanation = TextField(null=True, blank=True)
    problem = ForeignKey('tasks.Problem', CASCADE, related_name='examples')

    class Meta:
        ordering = ['id']


class Answers(Model):
    problem = ForeignKey('tasks.Problem', CASCADE)
    input = TextField()
    output = TextField(null=True)


class Submission(Model):
    class Status(TextChoices):
        PENDING = 'Pending'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'
    problem = ForeignKey('tasks.Problem', CASCADE)
    user = ForeignKey('users.User', CASCADE)
    status = CharField(max_length=15, choices=Status.choices)