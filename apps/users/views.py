from django.views.generic import DetailView, TemplateView, ListView

from users.models import Interview, Step
from .models import Blog


class BlogTemplateDetailView(TemplateView):
    queryset = Blog.objects.all()
    template_name = "users/blogs/blog-detail.html"


class CourseTemplateView(TemplateView):
    template_name = 'users/courses/course.html'


class InterviewListView(ListView):
    queryset = Interview.objects.all()
    template_name = "users/interviews/interview.html"
    context_object_name = "interviews"


class InterviewDetailView(DetailView):
    queryset = Interview.objects.all()
    template_name = "users/interviews/interview-detail.html"
    context_object_name = "interview"


class BlogTemplateView(ListView):
    queryset = Blog.objects.all()
    template_name = 'users/blogs/blog.html'
    context_object_name = 'blogs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['blog_detail'] = Step.objects.all()
        return context


class MainTemplateView(TemplateView):
    template_name = 'users/main/main.html'


class RegisterTemplateView(TemplateView):
    template_name = 'users/auth/register.html'


class LoginTemplateView(TemplateView):
    template_name = 'users/auth/login.html'
