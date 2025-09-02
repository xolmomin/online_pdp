import re

from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField

from shared.models import CreatedBaseModel, UUIDBaseModel
from shared.manager import UserManager


class User(AbstractUser, UUIDBaseModel):
    class Role(TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    username = None
    phone = CharField(max_length=15, null=True, unique=True)
    role = CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def check_phone(self):
        pattern = re.compile(
            r'^(?:\+?998[\s-]*)?(\d{2})[\s-]*(\d{3})[\s-]*(\d{2,4})(?:[\s-]*(\d{2}))?$'
        )
        m = pattern.match(self.phone)
        if not m:
            raise ValueError(f"Invalid UZ number: {self.phone}")
        parts = [g for g in m.groups() if g]  # keep only non-empty groups
        return "".join(parts)

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
    start_at = DateTimeField(auto_now_add=True)
    finish_at = DateTimeField()