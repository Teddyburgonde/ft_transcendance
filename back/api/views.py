from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils.decorators import method_decorator


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

@method_decorator(csrf_exempt, name='dispatch')
class CheckDataView(View):
	def post(self, request):
		nickname = request.POST.get('nickname')
		password = request.POST.get('password')
		try:
			user = User.objects.get(nickname=nickname)
			if user.password == password:  # À sécuriser avec un hachage
				return JsonResponse({"status": "success", "message": "Connexion réussie"})
			else:
				return JsonResponse({"status": "error", "message": "Mot de passe incorrect"})
		except User.DoesNotExist:
			return JsonResponse({"status": "error", "message": "Utilisateur introuvable"})

def index(request):
    return render(request, 'index.html')