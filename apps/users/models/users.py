import re

from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField

from shared.manager import UserManager
from shared.models import CreatedBaseModel, UUIDBaseModel


class User(AbstractUser, UUIDBaseModel):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    username = None
    phone = CharField(max_length=15, unique=True)
    type = CharField(max_length=20, choices=Type.choices, default=Type.STUDENT)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def check_phone(self):
        pattern = re.compile(r'^(?:\+?998[\s-]*)?(\d{2})[\s-]*(\d{3})[\s-]*(\d{2,4})(?:[\s-]*(\d{2}))?$')
        m = pattern.match(self.phone)
        if not m:
            raise ValueError(f"Invalid UZ number: {self.phone}")
        return "".join(g for g in m.groups() if g)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        if self.phone:
            self.phone = self.check_phone()
        super().full_clean(exclude, validate_unique, validate_constraints)


class UserCourse(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    user = ForeignKey('users.User', CASCADE)
    course = ForeignKey('users.Course', CASCADE)
    status = CharField(max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    started_at = DateTimeField(null=True, blank=True)
    finished_at = DateTimeField(null=True, blank=True)

# TODO https://api.dasturjon.uz/api/v1/proverb/public/random shu apidagi modelni yozish
