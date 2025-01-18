from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDestroy , CheckDataView, index

urlpatterns = [

    # Affiche le formulaire à /users/
    path('', index, name='index'),

    # Liste ou création d'utilisateurs
    path('list/', UserListCreate.as_view(), name="user-list-create"), 


    # Gestion d'un utilisateur spécifique
    path('<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name="user-retrieve-update-destroy"), 
    
    
    # Vérifie les identifiants utilisateur
    path('check/', CheckDataView.as_view(), name='check_data'),  
]
