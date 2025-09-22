from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from users.models import Interview
from .models import Blog, Step


class InterviewTemplateView(DetailView):
    queryset = Interview.objects.all()
    template_name = 'users/interview.html'


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    steps = Step.objects.filter(blog=blog)
    return render(request, "users/blog_detail.html", {"blog": blog, "steps": steps})
