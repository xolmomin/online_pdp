import json
import subprocess
import tempfile

from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView

from tasks.models import Problem, Topic
from tasks.checker.main import judge_submission
from tasks.models.tasks import Answers


class ProblemsListView(ListView):
    queryset = Problem.objects.all()
    template_name = 'users/tasks/task.html'
    paginate_by = 10
    context_object_name = 'problems'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


class ProblemDetailView(DetailView):
    queryset = Problem.objects.all()
    template_name = 'users/tasks/problem_detail.html'
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

            if not problem_id:
                return JsonResponse({"output": "❌ No problem ID provided."})

            test_cases = list(Answers.objects.filter(problem_id=problem_id).values('input', 'output'))
            judge_submission(code, Problem.objects.get(problem_id) ,test_cases)

            result = "✅ Submitted successfully and passed all tests!"

            return JsonResponse({"output": result})

        except Exception as e:
            return JsonResponse({"output": f"Error: {str(e)}"})
