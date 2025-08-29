from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField


class User(AbstractUser):
    class Role(TextChoices):
        VIEWER = 'viewer', 'Viewer'
        EDITOR = 'editor', 'Editor'

    phone = CharField(max_length=11, null=True, unique=True)
    role = CharField(max_length=255, choices=Role.choices, default=Role.VIEWER)