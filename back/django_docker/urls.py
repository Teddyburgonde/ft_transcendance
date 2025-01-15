from django.urls import re_path
from django.urls import path, include
from django.contrib import admin
from api.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('admin/', admin.site.urls),
    path('users/', include('api.urls')),
]
