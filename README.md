# ft_transcendance

## Version python

python --version <br>
Python 3.10.12

# Docker

Dockerfile pour Django 

```c
FROM python:3.10-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code Django
COPY . /app/

# Lancer Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
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
