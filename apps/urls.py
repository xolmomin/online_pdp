from django.urls import include, path

urlpatterns = [
    path('payments/', include('payments.urls')),
    path('', include('users.urls')),
]
