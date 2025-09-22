from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from users.models import User, Course, Lesson, Section, Topic, Blog, Interview, InterviewPart, Step


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


@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    readonly_fields = ('video_duration',)


class LessonStackedInline(NestedStackedInline):
    model = Lesson
    min_num = 0
    extra = 0


@admin.register(Section)
class SectionModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'
    inlines = LessonStackedInline,


class SectionNestedStackedInline(NestedStackedInline):
    model = Section
    min_num = 0
    extra = 0
    inlines = LessonStackedInline,


@admin.register(Course)
class CourseModelAdmin(NestedModelAdmin):
    list_display = 'id', 'name'
    readonly_fields = 'practice_count', 'rating', 'video_duration', 'video_count'
    inlines = SectionNestedStackedInline,


@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    pass


@admin.register(InterviewPart)
class PartModelAdmin(admin.ModelAdmin):
    pass


class InterviewStackedInline(admin.StackedInline):
    model = InterviewPart
    extra = 0
    min_num = 0


@admin.register(Interview)
class SectionInterviewModelAdmin(admin.ModelAdmin):
    inlines = InterviewStackedInline,


@admin.register(Step)
class StepModelAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)

# TODO bolimlar (Users, Blogs & Interview, Courses)
