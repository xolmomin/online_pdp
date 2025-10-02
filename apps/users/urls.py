from django.urls import path

from users.views import CourseTemplateView, InterviewListView, InterviewDetailView, \
    BlogTemplateView, MainTemplateView, BlogTemplateDetailView, RegisterTemplateView, LoginTemplateView

urlpatterns = [
    path('interviews', InterviewListView.as_view(), name='interview_list'),
    path('interview/<uuid:pk>', InterviewDetailView.as_view(), name='interview_detail'),
    path('courses', CourseTemplateView.as_view(), name='course_list'),
    path('blogs', BlogTemplateView.as_view(), name='blog_list'),
    path('blogs-detail', BlogTemplateDetailView.as_view(), name='blog_detail'),
    path('', MainTemplateView.as_view(), name='main'),
    path('register', RegisterTemplateView.as_view(), name='register'),
    path('login', LoginTemplateView.as_view(), name='login'),
]
