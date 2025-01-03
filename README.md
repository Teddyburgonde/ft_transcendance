# ft_transcendance

# Version python

python --version <br>
Python 3.10.12


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
