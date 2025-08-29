from django.urls import include, path

urlpatterns = [
    path('payments/', include('payments.urls')),
    path('users/', include('users.urls')),
]
