from django.urls import path

from tasks.views import ProblemsListView

urlpatterns = [
    path('problemset', ProblemsListView.as_view(), name='task_list'),
]