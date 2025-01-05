# ft_transcendance

## Version python

python --version <br>
Python 3.10.12

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
