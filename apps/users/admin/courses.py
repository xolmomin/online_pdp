import threading

from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from users.models import Course, Lesson, Section, Category, Blog, Interview, InterviewPart, Step
from users.utils import convert_video_to_hls


@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

    def save_model(self, request, obj, form, change):
        request.get_host()
        super().save_model(request, obj, form, change)
        threading.Thread(target=convert_video_to_hls(self.video.path, self.video.name, self.id))


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
    inlines = SectionNestedStackedInline,


@admin.register(Category)
class TopicModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'title'


@admin.register(InterviewPart)
class PartModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'interview__title'


class InterviewStackedInline(admin.StackedInline):
    model = InterviewPart
    extra = 0
    min_num = 0
    exclude = 'asked_by',


@admin.register(Interview)
class SectionInterviewModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',
    inlines = InterviewStackedInline,


@admin.register(Step)
class StepModelAdmin(admin.ModelAdmin):
    pass
