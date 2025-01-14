from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer

@api_view(["POST"])
def login(request):
    return Response({})

@api_view(["POST"])
def signup(request):
    return Response({})

@api_view(["GET"])
def test_token(request):
    return Response({})

class UserListCreate(generics.ListCreateAPIView):
    """
    Gère :
    - Liste des utilisateurs (GET)
    - Création d'un utilisateur (POST)
    - Suppression de tous les utilisateurs (DELETE)
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        nickname = self.request.query_params.get("nickname", "").strip()
        if nickname:
            return User.objects.filter(nickname__icontains=nickname)
        return User.objects.all()

    def delete(self, request, *args, **kwargs):
        User.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Gère :
    - Récupération d'un utilisateur spécifique (GET)
    - Mise à jour (PUT/PATCH)
    - Suppression (DELETE)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
