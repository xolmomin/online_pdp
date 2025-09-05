from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from users.models import Course, Lesson, Section, Topic


@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "usable_password", "password1", "password2"),
            },
        ),
    )
    ordering = ('phone',)

@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Section)
class SectionModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    pass


"""
online.pdp
boomstream (video hosting)

vdcipher

"""