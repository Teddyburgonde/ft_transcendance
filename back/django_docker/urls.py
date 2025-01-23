from django.urls import path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from api import views 
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('api.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('enable-2fa/', views.enable_2fa, name='enable_2fa'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
	path('i18n/', include('django.conf.urls.i18n')),
	path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
