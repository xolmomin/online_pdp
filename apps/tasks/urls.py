from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from tasks.views import ProblemsListView, ProblemDetailView, RunCodeView, SubmitCodeView

urlpatterns = [
    path('problemset', ProblemsListView.as_view(), name='problem_list'),
    path('problemset/<int:pk>', ProblemDetailView.as_view(), name='problem_detail'),
    path('runcode', RunCodeView.as_view(), name='run_code'),
    path('submit/code', csrf_exempt(SubmitCodeView.as_view()), name='submit_code'),
]