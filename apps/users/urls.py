from django.urls import path

from users.views import CourseListView, InterviewListView, InterviewDetailView, \
    BlogListView, MainListView, BlogDetailView, RegisterTemplateView, LoginTemplateView, \
    CourseDetailView, KeyDeliveryView, LessonVideoView

urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('interviews', InterviewListView.as_view(), name='interview_list'),
    path('interviews/<uuid:pk>', InterviewDetailView.as_view(), name='interview_detail'),
    path('courses', CourseListView.as_view(), name='course_list'),
    path('courses/<uuid:pk>', CourseDetailView.as_view(), name='course_detail'),
    path('blogs', BlogListView.as_view(), name='blog_list'),
    path('blogs/<uuid:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('auth/register', RegisterTemplateView.as_view(), name='register'),
    path('auth/login', LoginTemplateView.as_view(), name='login'),
    # path('lesson/<uuid:pk>/', LessonVideoView.as_view(), name='lesson_video'),
    # path('get_key/lesson/<uuid:lesson_uuid>/', KeyDeliveryView.as_view(), name='lesson_key'),
]
