from django.shortcuts import redirect
from django.urls import path
from .views import UserListCreate, redirect_to_intra, UserRetrieveUpdateDestroy , CheckDataView, index

urlpatterns = [

    # Affiche le formulaire à /users/
    path('', index, name='index'),

    # Liste ou création d'utilisateurs
    path('list/', UserListCreate.as_view(), name="user-list-create"), 


    # Gestion d'un utilisateur spécifique
    path('<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name="user-retrieve-update-destroy"), 
    
    
    # Vérifie les identifiants utilisateur
    path('check/', CheckDataView.as_view(), name='check_data'),  
    path('auth/callback/', CheckDataView.as_view(), name='auth_callback'),
    path('users/check/', CheckDataView.as_view(), name='check_data'),
    path('auth/intra/', redirect_to_intra, name='redirect_to_intra'),
]
