from django.views.generic import ListView

from tasks.models import Problem, Topic


class ProblemsListView(ListView):
    queryset = Problem.objects.order_by('id')
    template_name = 'users/tasks/task.html'
    paginate_by = 10
    context_object_name = 'problems'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context