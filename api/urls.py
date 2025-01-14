from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDestroy#, UserList

urlpatterns = [
    
    # Lister et créer des utilisateurs
    path('', UserListCreate.as_view(), name="user-list-create"),


    # Détails, mise à jour ou suppression d’un utilisateur via pk
    path('<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name="user-retrieve-update-destroy"),
]

