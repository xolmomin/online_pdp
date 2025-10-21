from django.views.generic import DetailView, TemplateView, ListView

from users.models import Interview, Step, Course, Section
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
        context['sections'] = self.object.courses.all()
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
    queryset = Course.objects.order_by('-created_at')[:6]
    template_name = 'users/main/main.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['blogs'] = Blog.objects.order_by('-created_at')[:3]
        return context


class RegisterTemplateView(TemplateView):
    template_name = 'users/auth/register.html'


class LoginTemplateView(TemplateView):
    template_name = 'users/auth/login.html'
