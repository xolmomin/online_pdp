from django.views.generic import DetailView, TemplateView, ListView

from users.models import Interview
from .models import Blog, Step



class BlogDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = "users/blogs/blog_detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = Step.objects.filter(blog=self.object)
        return context


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


class BlogTemplateView(TemplateView):
    template_name = 'users/blogs/blog.html'


class MainTemplateView(TemplateView):
    template_name = 'users/main/main.html'
