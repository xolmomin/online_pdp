from django.urls import path

from users.views import InterviewTemplateView, CourseTemplateView, InterviewCanvaListView, InterviewCanvaDetailView, \
    BlogTemplateView, MainTemplateView

urlpatterns = [
    path('interview/<uuid:pk>', InterviewTemplateView.as_view(), name='interview_page'),
    path('interview-canva', InterviewCanvaListView.as_view(), name='interview_list'),
    path('interview-canva/<uuid:pk>', InterviewCanvaDetailView.as_view(), name='interview_detail'),
    path('courses', CourseTemplateView.as_view(), name='course_list'),
    path('blogs', BlogTemplateView.as_view(), name='blog_list'),
    path('main', MainTemplateView.as_view(), name='main'),
]
