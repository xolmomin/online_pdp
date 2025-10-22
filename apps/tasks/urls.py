from django.urls import path

from tasks.views import ProblemsListView, ProblemDetailView

urlpatterns = [
    path('problemset', ProblemsListView.as_view(), name='problem_list'),
    path('problemset/<int:pk>', ProblemDetailView.as_view(), name='problem_detail'),
]