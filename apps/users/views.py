import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from django.views.generic import DetailView, TemplateView, ListView

from users.models import Interview, Step, Course, Lesson
from .models import Blog


class BlogListView(ListView):
    queryset = Blog.objects.all()
    template_name = 'users/blogs/blog.html'
    context_object_name = 'blogs'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_detail'] = Step.objects.all()
        return context


class BlogDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'users/blogs/blog-detail.html'
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = self.object.steps.all()
        return context


class CourseListView(ListView):
    queryset = Course.objects.all()
    template_name = 'users/courses/course.html'
    context_object_name = 'courses'
    paginate_by = 2


class CourseDetailView(DetailView):
    template_name = 'users/courses/course-detail.html'
    queryset = Course.objects.all()
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InterviewListView(ListView):
    queryset = Interview.objects.all()
    template_name = "users/interviews/interview.html"
    context_object_name = "interviews"
    paginate_by = 1


class InterviewDetailView(DetailView):
    queryset = Interview.objects.all()
    template_name = "users/interviews/interview-detail.html"
    context_object_name = "interview"


class MainListView(ListView):
    queryset = Course.objects.all()[:6]
    template_name = 'users/main.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['blogs'] = Blog.objects.all()[:3]
        return context


class RegisterTemplateView(TemplateView):
    template_name = 'users/auth/register.html'


class LoginTemplateView(LoginView):
    template_name = 'users/auth/login.html'
    next_page = reverse_lazy('main')


# TODO Video view


class KeyDeliveryView(LoginRequiredMixin, View):
    """
    Faqat login foydalanuvchiga video kalitni beradi (UUID versiya).
    """

    def get(self, request, lesson_uuid):
        try:
            base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', f'lesson_{lesson_uuid}')
            key_path = os.path.join(base_dir, 'enc.key')
            with open(key_path, 'rb') as f:
                key_data = f.read()
        except FileNotFoundError:
            raise Http404("Kalit topilmadi")

        response = HttpResponse(key_data, content_type='application/octet-stream')
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        return response


class LessonVideoView(DetailView):
    model = Lesson
    template_name = 'users/courses/'  # TODO
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['m3u8_url'] = Lesson.objects.first().video_link
        return context


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/auth/profile.html'
