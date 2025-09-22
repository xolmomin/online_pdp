from django.urls import path

from users.views import InterviewTemplateView

urlpatterns = [
    path('interview/<uuid:pk>', InterviewTemplateView.as_view(), name='interview_page'),
]
