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
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login 
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

CLIENT_ID = config("INTRA_CLIENT_ID")
CLIENT_SECRET = config("INTRA_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080/auth/callback/"


def redirect_to_intra(request):
    intra_url = f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(intra_url)

def login_view(request):
    if request.method == 'POST':
        # Récupère le nom d'utilisateur et le mot de passe
        username = request.POST.get('nickname')
        password = request.POST.get('password')

        # Utilise la fonction authenticate pour vérifier le nom d'utilisateur et le mot de passe
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si l'utilisateur est authentifié, on le connecte et on le redirige vers /enable-2fa
            login(request, user)
            return redirect('enable_2fa')  # Redirige vers la page pour configurer 2FA
        else:
            # Si l'utilisateur ou le mot de passe est incorrect, on affiche un message d'erreur
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
            return render(request, 'index.html')  # Redirige vers la page de login avec un message d'erreur

    return render(request, 'index.html')

@login_required
def verify_2fa(request):
    if request.method == 'POST':
        token = request.POST.get('token')  # Le code 2FA entré par l'utilisateur
        user = request.user  # L'utilisateur connecté
        
        # Vérifie si l'utilisateur a un appareil TOTP
        try:
            totp_device = TOTPDevice.objects.get(user=user)
        except TOTPDevice.DoesNotExist:
            messages.error(request, "Aucun appareil 2FA trouvé.")
            return redirect('enable_2fa')  # Redirige vers la page pour configurer 2FA si aucun appareil n'est trouvé

        # Vérifie le token
        if totp_device.verify_token(token):
            # Si le token est valide, redirige vers la page de félicitations
            return redirect('success_page')  # Remplace 'success_page' par le nom de l'URL de la page de félicitations

        # Si le token est invalide
        messages.error(request, "Code invalide. Essayez à nouveau.")
        return render(request, 'verify_2fa.html')

    return render(request, 'verify_2fa.html')

@login_required
def enable_2fa(request):
    user = request.user
    # Créer ou récupérer l'appareil TOTP de l'utilisateur
    totp_device, created = TOTPDevice.objects.get_or_create(user=user)

    # Obtenir l'URL pour générer le QR Code
    qr_url = totp_device.config_url  # L'URL du QR code

    # Générer le QR code
    img = qrcode.make(qr_url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Sauvegarder l'image du QR code dans le dossier MEDIA
    image_name = f'{user.username}_qrcode.png'
    file_path = default_storage.save(image_name, ContentFile(img_io.read()))

    # Générer l'URL pour l'image du QR code
    qr_image_url = default_storage.url(file_path)

    # Passer l'URL de l'image au template
    return render(request, 'enable_2fa.html', {'qr_image_url': qr_image_url})

@login_required
def success_page(request):
    # Cette vue sera appelée après une connexion réussie
    return render(request, 'success_page.html')


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
        # Cette vue peut gérer une connexion OAuth ou retourner un message de connexion réussie
        code = request.GET.get("code")
        if code:
            # Traitement pour l'OAuth
            return JsonResponse({"status": "success", "message": "Connexion réussie avec OAuth"})
        
        # Si la vérification échoue
        return JsonResponse({"status": "error", "message": "Échec de la connexion"})

    def post(self, request):
        # Traitement de la connexion via formulaire
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(nickname=nickname)
            if user.check_password(password):  # Utilisation de la méthode check_password() pour vérifier le mot de passe
                return JsonResponse({"status": "success", "message": "Connexion réussie"})
            else:
                return JsonResponse({"status": "error", "message": "Mot de passe incorrect"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Utilisateur introuvable"})

def index(request):
	current_language = get_language()  # Récupère la langue active
	return render(request, 'index.html', {'LANGUAGE_CODE': current_language})