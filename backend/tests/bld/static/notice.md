# Notice d'utilisation

## Un onglet [recherche](search)

Dans la barre de recherche, on peut effectuer une recherche par mots-clefs avec des **opérateurs spéciaux**:
La recherche : ("moteur de recherche" -python) OR (Docker +backend) retournera les documents avec la séquence "moteur de recherche" sans python OU les documents avec Docker et backend.

On peut aussi mettre un filtre par tag.

Les documents sont présentés par ordre de pertinence. En mode **admin**, il est possible de le supprimer ou de changer des méta-données.
Une limite est indiquée pour les documents jugés non pertinents.

## Un onglet [glossaire](glossary)

La liste des **acronymes** avec une barre de recherche. En mode **admin**, possibilité de supprimer, modifier ou ajouter des éléments. Les "\_" sont ajoutés automatiquement, les accents et les mots de liaison sont supprimés.

## Un onglet [expression](expression)

Idem que pour les acronymes.

## Un onglet [admin 👤](admin)

Il est visible uniquement en mode **admin**. On peut ajouter un nouveau document, lancer la réindexation, ajouter des pièces-jointes ou changer les seuils d'affichage et de pertinence.

##  Une icône de connexion
Un clic ouvre ou ferme la **fenêtre d'identification**. Pour devenir admin, rentrez user1 et abcxyz pour tester.

---
# Briques technologiques

## Le moteur de recherche
Le coeur du moteur s'appuie sur la technologie ouverte [**elasticsearch**](https://elasticsearch.com).

## L'interface utilisateur
ELle est développée en [Svelte](https://svelte.dev), un language récent et très rapide qui compile du javascript, html et css.
Le site est servi avec Nginx, pour contrôler les connexions et gérer le routage des services appelés par l'interface.

## Le serveur
Le serveur qui répond aux requêtes de l’interface est développée en **Python**, avec la bibliothèque Flask.

## Autres outils
Pour mieux cloisonner les différents services, nous utilisons **Docker**.
