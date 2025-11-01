import re

from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField

from users.models import User


def check_phone(phone):
    pattern = re.compile(r'^(?:\+?998[\s-]*)?(\d{2})[\s-]*(\d{3})[\s-]*(\d{2,4})(?:[\s-]*(\d{2}))?$')
    m = pattern.match(phone)
    if not m:
        raise ValueError(f"Invalid UZ number: {phone}")
    return "".join(g for g in m.groups() if g)


class CostumeUserCreationForm(UserCreationForm):
    first_name = CharField()
    last_name = CharField()
    phone = CharField(validators=[])
    email = EmailField()

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone', 'email',
