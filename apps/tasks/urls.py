from django.urls import path

from tasks.views import ProblemsListView, ProblemDetailView, RunCodeView

urlpatterns = [
    path('problemset', ProblemsListView.as_view(), name='problem_list'),
    path('problemset/<int:pk>', ProblemDetailView.as_view(), name='problem_detail'),
    path('runcode', RunCodeView.as_view(), name='run_code'),
    path('submitcode', RunCodeView.as_view(), name='submit_code'),
]