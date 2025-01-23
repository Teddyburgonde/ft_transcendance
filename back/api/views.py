from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from django.utils.translation import get_language
import requests 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
from io import BytesIO 
from django.core.files.storage import default_storage 
from django.core.files.base import ContentFile

CLIENT_ID = config("INTRA_CLIENT_ID")
CLIENT_SECRET = config("INTRA_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080/auth/callback/"


def redirect_to_intra(request):
    intra_url = f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(intra_url)


@login_required
def verify_2fa(request):
    if request.method == 'POST':
        token = request.POST.get('token')  # Le code 2FA entré par l'utilisateur
        user = request.user
        
        # Vérifie si le code est valide
        totp_device = TOTPDevice.objects.get(user=user)
        if totp_device.verify_token(token):
            # Si le code est valide, redirige l'utilisateur vers une page de succès ou une autre page
            return redirect('home')  # Par exemple, rediriger vers la page d'accueil

        # Si le code est invalide, affiche un message d'erreur
        return render(request, 'verify_2fa.html', {'error': 'Code invalide. Essayez à nouveau.'})

    return render(request, 'verify_2fa.html')

@login_required
def enable_2fa(request):
    user = request.user
    # Crée ou récupère l'appareil TOTP de l'utilisateur
    totp_device, created = TOTPDevice.objects.get_or_create(user=user)

    # Obtenir l'URL pour générer le QR Code
    qr_url = totp_device.config_url  # L'URL du QR code
    
    # Générer l'image du QR code avec une taille plus grande
    img = qrcode.make(qr_url, box_size=10, border=4)  # box_size plus grand pour améliorer la taille de l'image

    # Sauvegarder l'image en mémoire
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Créer un nom de fichier temporaire pour l'image
    image_name = f'{user.username}_qrcode.png'
    file_path = default_storage.save(image_name, ContentFile(img_io.read()))

    # Générer l'URL de l'image du QR code
    qr_image_url = default_storage.url(file_path)

    # Passer l'URL de l'image au template
    return render(request, 'enable_2fa.html', {'qr_image_url': qr_image_url})


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