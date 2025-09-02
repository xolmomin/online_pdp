from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = 'viewer', 'Viewer'
        MODERATOR = 'moderator', 'Viewer'
        TEACHER = 'teacher', 'Viewer'
        STUDENT = 'viewer', 'Viewer'

    username = None
    phone = CharField(max_length=11, null=True, unique=True)
    role = CharField(max_length=255, choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = ['phone']
    REQUIRED_FIELDS = []

    objects = UserManager()
