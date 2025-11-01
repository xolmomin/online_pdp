import json
import subprocess
import tempfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView

from tasks.models import Problem, Topic
from tasks.models.tasks import Submission
from tasks.utils import judge_submission


class ProblemsListView(ListView):
    queryset = Problem.objects.all()
    template_name = 'tasks/task.html'
    paginate_by = 10
    context_object_name = 'problems'

    def get_queryset(self):

        # Handle search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = self.queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(topics__name__icontains=search_query)
            ).distinct()

        # Handle topic filtering
        topic_slug = self.request.GET.get('topic')
        if topic_slug:
            queryset = self.queryset.filter(topics__slug=topic_slug).distinct()

        return self.queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


class ProblemDetailView(DetailView):
    queryset = Problem.objects.all()
    template_name = 'tasks/problem_detail.html'
    context_object_name = 'problem'


class RunCodeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")

            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
                temp.write(code.encode())
                temp.flush()

                try:
                    output = subprocess.check_output(
                        ["python3", temp.name],
                        stderr=subprocess.STDOUT,
                        timeout=3
                    )
                    return JsonResponse({"output": output.decode()})
                except subprocess.CalledProcessError as e:
                    return JsonResponse({"output": e.output.decode()})
                except subprocess.TimeoutExpired:
                    return JsonResponse({"output": "Error: Code execution timed out."})

        except Exception as e:
            return JsonResponse({"output": f"Error: {str(e)}"})


class SubmitCodeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            problem_id = data.get("problem_id")

            problem = Problem.objects.filter(pk=problem_id).first()

            if not problem:
                return JsonResponse({"output": "❌ Problem not found."})

        except Exception as e:
            return JsonResponse({"output": f"Error: {str(e)}"})

        try:

            results = judge_submission(code, problem.pk)

            failed = next((r for r in results if r["verdict"] != "AC"), None)

            if failed:
                verdict = failed["verdict"]
                test_num = failed["testcase"]
                msg = f"❌ Test #{test_num} failed ({verdict})"
                status = Submission.Status.REJECTED
            else:
                msg = "✅ All tests passed!"
                status = Submission.Status.ACCEPTED

            output = msg
            results = results

        except Exception as e:
            output = f"Error: {str(e)}"
            results = None
            status = Submission.Status.REJECTED

        Submission.objects.create(
            status=status,
            problem=problem,
            user=request.user,
            language_id=1
        )

        return JsonResponse({
            "output": output,
            "results": results
        })
