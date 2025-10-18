from django.urls import path

from users.views import CourseListView, InterviewListView, InterviewDetailView, \
    BlogListView, MainListView, BlogDetailView, RegisterTemplateView, LoginTemplateView, \
    CourseDetailTemplateView

urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('interviews', InterviewListView.as_view(), name='interview_list'),
    path('interview/<uuid:pk>', InterviewDetailView.as_view(), name='interview_detail'),
    path('courses', CourseListView.as_view(), name='course_list'),
    path('course-detail', CourseDetailTemplateView.as_view()),
    path('blogs', BlogListView.as_view(), name='blog_list'),
    path('blog/<uuid:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('register', RegisterTemplateView.as_view(), name='register'),
    path('login', LoginTemplateView.as_view(), name='login'),
]
