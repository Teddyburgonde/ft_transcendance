from django.urls import path, include
from django.contrib import admin
# from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('i18n/', include('django.conf.urls.i18n')),  # Pour le multilingue
   # path('', include('django.contrib.auth.urls')),  # Authentification de base
    #path('account/', include('two_factor.urls')),  # Routes pour le 2FA

    # path('', include('api.urls')),  # Routes spécifiques à ton app "api"

	path('account/', include(('two_factor.urls', 'two_factor'))),
]

# print("URL patterns:", urlpatterns)