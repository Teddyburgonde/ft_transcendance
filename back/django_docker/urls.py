from typing import List, Union
from django.urls import path, include, URLPattern, URLResolver
from django.contrib import admin
from two_factor.admin import AdminSiteOTPRequired

# Appliquer l'OTP à l'interface d'administration
admin.site.__class__ = AdminSiteOTPRequired

# Définir les types pour URLList
URL = Union[URLPattern, URLResolver]
URLList = List[URL]

# Définir les URL patterns
urlpatterns: URLList = [
    path('admin/', admin.site.urls),
    path('account/', include('two_factor.urls', namespace='two_factor')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('api.urls')),
]