# ft_transcendance

## Version python

python --version <br>
Python 3.10.12

## Faire une migration

Une migration permet de mettre a jour ta base de donnée par rapport a ton model. 
Si dans ton model tu modifie un champ tu dois tout de suite faire une migration.
Par exemple dans ton model tu ajoues un nickname , la base de donnée lui il n'a pas connaissance de ce nouveau ajout donc on doit faire une migration.

```c
python3 manage.py makemigrations
python manage.py migrate
```

# Lancer un server

python manage.py runserver


# Aller sur Django Rest framework 

http://127.0.0.1:8000/users/

# Docker

**1. Ajouter un Dockerfile a ton projet Django.**
Dockerfile pour Django : 

```c
# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /app 
# Install system dependencies
RUN apk update
RUN apk add \
	pkgconfig \
	gcc \
	musl-dev \
	bash \
	mariadb-dev

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . /app
# Run server
ENTRYPOINT [ "python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
```

**2. Créer une image Docker**

Tape dans ton terminal 
```c
docker build -t mon-projet .
```
Une fois terminé, tu obtiens une image nommée mon-projet.

**3. Verifier l'image construite**

Tape dans ton terminal :
```c
docker images
```
Tu devrais voir une ligne ressemblant a ceci : 

```c
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
mon-projet      latest    <IMAGE_ID>     <SOME_TIME>      <SIZE>
```

**4. lancer un conteneur a partir de l'image :**

```c
docker run -d -p 8000:8000 mon-projet
```

**5. Lancer le localhost 

```c
http://localhost:8000
```

** 6.Et admirer votre site =)** 


**Envoyer l'image a un collegue** 

Sur ton ordinateur tape dans le terminal :

```c
docker save -o mon-projet.tar mon-projet
```

**Envoie a ton collegue le fichier generer.**

Sur son ordinateur il doit taper : 
```c
docker load -i mon-projet.tar
```

**Puis il peut lancer :** 
```c
docker run -d -p 8000:8000 mon-projet
```

**Et il se connectera sur :** 

```c
http://localhost:8000
```


Dockerfile pour Nginx

```c
FROM nginx:alpine

# Copier la configuration Nginx
COPY nginx.conf /etc/nginx/nginx.conf
```

nginx.conf (a revoir je pense qu'il peut avoir des erreurs ) <br>

```c
server {
	listen 80;

	location / {
		proxy_pass http://web:8000;  # Le container Gunicorn
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
}
```

docker-compose.yml
```c
version: '3.8'
services:
  web:
	build:
	  context: .
	  dockerfile: Dockerfile
	ports:
	  - "8000:8000"
	depends_on:
	  - db

  nginx:
	build:
	  context: .
	  dockerfile: Dockerfile.nginx
	ports:
	  - "80:80"
	depends_on:
	  - web

  db:
	image: postgres:14
	environment:
	  POSTGRES_USER: myuser
	  POSTGRES_PASSWORD: mypassword
	  POSTGRES_DB: mydb
```

# Back

## Serialization
Converti une class en format JSON comme <br>
ça la base de donnée comprends les requettes.


```py
fron rest_frameworkd import serializers
front .models import Eleve

class EleveSerializer(serializers.ModelSerializer): 
  class Meta:
	model = Eleve 
	fields = ["id", "title", "content"]
```



## FRONT

## Les différentes méthodes :

Le front, lorsqu’il veut communiquer avec le back, envoie des requêtes HTTP.
Prenons un exemple avec Instagram :
Sur ton Instagram, tu as des photos. C’est la partie visuelle de ton site (le front).
Si tu veux supprimer une photo, le front envoie une requête DELETE à l’API du back.
Le back reçoit cette requête et dit : "Tu m’as demandé de supprimer cette donnée, donc je la supprime."
Et hop, la photo est supprimée à la fois du site et de la base de données.

## GET (récupérer des données)

```js
fetch('https://api.example.com/data')
  .then(response => response.json()) // Transforme la réponse en JSON
  .then(data => console.log('Données reçues :', data))
  .catch(error => console.error('Erreur lors du GET :', error));
```

## POST (envoyer des données pour en créer de nouvelles)

```js
fetch('https://api.example.com/data', {
  method: 'POST',
  headers: {
	'Content-Type': 'application/json',
  },
  body: JSON.stringify({ key: 'value' }), // Données envoyées au serveur
})
  .then(response => response.json())
  .then(data => console.log('Ressource créée :', data))
  .catch(error => console.error('Erreur lors du POST :', error));
```

## PUT (mettre à jour ou remplacer une ressource)

```js

fetch('https://api.example.com/data/1', {
  method: 'PUT',
  headers: {
	'Content-Type': 'application/json',
  },
  body: JSON.stringify({ key: 'newValue' }), // Données mises à jour
})
  .then(response => response.json())
  .then(data => console.log('Ressource mise à jour :', data))
  .catch(error => console.error('Erreur lors du PUT :', error));

```

## DELETE (supprimer une ressource)

```js
fetch('https://api.example.com/data/1', {
  method: 'DELETE',
})
  .then(response => {
	if (response.ok) {
	  console.log('Ressource supprimée avec succès');
	} else {
	  console.error('Erreur lors de la suppression');
	}
  })
  .catch(error => console.error('Erreur lors du DELETE :', error));
```

# Base de donnée

## Creation d'une base de donnée (PostgreSql)

Installer PostgreSql puis : 
```c
sudo service postgresql start
sudo -u postgres psql
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

##  Exporter la base de données et l'importer chez toi

Crée un fichier mydatabase_dump.sql contentant toutes les données et la structure de ta base.

```c
pg_dump -U myuser -d mydatabase > mydatabase_dump.sql
```
Met ce fichier sur ton ordinateur chez toi puis
créer une base vide avec :
```c
CREATE DATABASE mydatabase;
```

Creer une utilisateur (si necessaire).
```c
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

puis restaure la sauvegarde :
```c
psql -U myuser -d mydatabase < mydatabase_dump.sql
```

# Front 

## Creation d'un formulaire en 5 étapes 

1. Cree un formulaire 

Ceci est un formulaire qui est dans une card (La card c'est uniquement pour le design). <br> 
il y a 3 champs important : Le label Nickmame , le label Password , et la methode POST <br>

```html
<div class="container-fluid d-flex justify-content-center align-items-center vh-100">
	<!-- Centered Card -->
	<div class="card" style="width: 24rem;">
	<div class="card-body">
	  <h5 class="card-title text-center">Login</h5>
	  <form id="login-form" method="POST" action="http://127.0.0.1:8080/users/check/">
	  <div class="mb-3">
		<label for="formGroupExampleInput" class="form-label">Nickname</label>
		<input type="text" class="form-control" id="formGroupExampleInput" name="nickname">
	  </div>
	  <div class="mb-3">
		<label for="exampleInputPassword1" class="form-label">Password</label>
		<input type="password" class="form-control" id="exampleInputPassword1" name="password">
	  </div>
	  <div class="mb-3 form-check">
		<input type="checkbox" class="form-check-input" id="exampleCheck1">
		<label class="form-check-label" for="exampleCheck1">Remember me</label>
	  </div>
	  <button type="submit" class="btn btn-primary w-100">Submit</button>
	  </form>
	</div>
	</div>
  </div>
```
Ce formulaire utilise une requete POST : <br>
Le client envoie une requête POST, cette requête arrive à l'URL,<br>
qui est un endpoint de l'API. Le backend vérifie si les données<br>
envoyées correspondent à celles déjà présentes dans la base de <br>
données. Si oui, il retourne une réponse comme "Connexion réussie".<br>


2. Configuration des URLS 

Étape 2 : Configuration des URLs

Ajouté une route dans urls.py pour afficher le formulaire via une vue index. <br>

```python
from django.urls import path
from .views import index

urlpatterns = [

path('', index, name='index'),

]
```

Une autre route pour la vérification des données via le backend. <br>

```python
from django.urls import path
from .views import CheckDataView

urlpatterns = [

path('check/', CheckDataView.as_view(), name='check_data'),

]
```

Relation entre les deux : 
- Une pour afficher le formulaire (index).
- Une pour traiter les données envoyées (check).

3. Création des vues Django

- Dans views.py , definir une vue pour afficher le formulaire 

```python

def index(request):
	return render(request, 'index.html')
```

- Dans views.py , definir une vue pour récupérer les données envoyées par le formulaire et les comparer à celles de la base de données.

```python 
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
```
4. Etape liaison entre le formulaire et le backend 

<form id="login-form" method="POST" action="http://127.0.0.1:8080/users/check/">

5. Gestion des réponses 

dans views.py 

```python
return JsonResponse({"status": "success", "message": "Connexion réussie"})
return JsonResponse({"status": "error", "message": "Mot de passe incorrect"})
return JsonResponse({"status": "error", "message": "Utilisateur introuvable"})
```
# Jeton CSRF pour proteger le back end

1. Ajoute de la balise jeton  
Dans le formulaire rajouter

```html
<form id="login-form" method="POST" action="http://127.0.0.1:8080/users/check/">
{% csrf_token %} #Le jeton 
<div class="mb-3">
```

# Rendre son site bilingue

1. Activer le système de traduction dans settings.py.
Dans settings.py 

```python
LANGUAGE_CODE = 'en'  # Langue par défaut
USE_I18N = True  # Active les traductions
LANGUAGES = [
	('en', 'English'),
	('fr', 'Français'),
]
```

2. Ajouter LocaleMiddleware dans les middlewares. 
Dans settings py

```python
MIDDLEWARE = [
	'django.middleware.locale.LocaleMiddleware',  
]
```


3. Configurer les chemins des fichiers de traduction (facultatif)

```python
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

3. Marquer les textes à traduire dans les templates et le backend ({% trans %} et _()).

```html
<a class="navbar-brand mx-auto" href="#">{% trans "Welcome" %}</a>
```

4. Générer les fichiers de traduction avec makemessages. 

Dans le terminal 

```c
django-admin makemessages -l fr
```
Cela crée un fichier de traduction pour le français dans locale/fr/LC_MESSAGES/django.po.

5. Remplir les traductions dans les fichiers .po.

```c
msgid "Welcome"
msgstr "Bienvenue"
```
6. Compiler les fichiers de traduction avec compilemessages.

```c
django-admin compilemessages
```

7. Ajouter un sélecteur de langue dans les templates.

dans urls.py 

from django.conf.urls.i18n import i18n_patterns

```python
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Gestion de la langue
]
```

8. Configurer les URL pour le changement de langue.
9. Tester le fonctionnement bilingue sur le site.

