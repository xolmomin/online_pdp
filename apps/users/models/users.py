from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = 'viewer', 'Viewer'
        MODERATOR = 'moderator', 'Viewer'
        TEACHER = 'teacher', 'Viewer'
        STUDENT = 'viewer', 'Viewer'

    phone = CharField(max_length=11, null=True, unique=True)
    role = CharField(max_length=255, choices=Role.choices, default=Role.STUDENT)
