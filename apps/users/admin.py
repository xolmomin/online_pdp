from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, Course, Lesson, Section, Topic, Blog, SectionInterview, Part, Step


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
    list_display = ('id', 'name',)
    readonly_fields = ('practice_count', 'rating', 'video_duration', 'video_count')


@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    readonly_fields = ('video_duration',)


@admin.register(Section)
class SectionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    pass


@admin.register(SectionInterview)
class SectionInterviewModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Part)
class PartModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepModelAdmin(admin.ModelAdmin):
    pass


"""
online.pdp
boomstream (video hosting)

vdcipher

"""
