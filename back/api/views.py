from django.shortcuts import redirect 
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from decouple import config
from django.utils.translation import get_language
import requests 



CLIENT_ID = config("INTRA_CLIENT_ID")
CLIENT_SECRET = config("INTRA_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080/auth/callback/"


def redirect_to_intra(request):
    intra_url = f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(intra_url)

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

class CheckDataView(View):
	def get(self, request):
		# Cas 1 : Retour d'Intra 42 avec OAuth (GET avec un code)
		code = request.GET.get("code")
		if code:
			# Échanger le code contre un token d'accès
			token_url = "https://api.intra.42.fr/oauth/token"
			data = {
				"grant_type": "authorization_code",
				"client_id": CLIENT_ID,
				"client_secret": CLIENT_SECRET,
				"code": code,
				"redirect_uri": REDIRECT_URI,
			}
			response = requests.post(token_url, data=data)
			if response.status_code == 200:
				access_token = response.json().get("access_token")
				return JsonResponse({"status": "success", "message": "Connexion via Intra réussie", "token": access_token})
			else:
				return JsonResponse({"status": "error", "message": "Échec de la connexion via Intra"})
		else:
			return JsonResponse({"status": "error", "message": "Code OAuth manquant"})

	def post(self, request):
		# Cas 2 : Connexion normale via formulaire
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
	current_language = get_language()  # Récupère la langue active
	return render(request, 'index.html', {'LANGUAGE_CODE': current_language})