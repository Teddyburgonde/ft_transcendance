from django.urls import re_path
from django.urls import path, include
from django.contrib import admin
from api import views

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),    
    path('admin/', admin.site.urls),
    path('users/', include('api.urls')),
]
