_Dépot boite à outils pour un moteur de recherche._


## Présentation
 Makefile : Contient les commandes et variables du projet.<br />
 |_ elasticsearch : Fichiers de config pour **ElasticSearch**.<br />
 |_ backend : Serveur **Flask** et indexation de la base ouverte [bonnes feuilles](https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles) pour tester le moteur.<br />
 |_ frontend : Code source pour distribuer une interface utilisateur branché à ElasticSearch. Fourni un site statique en **Svelte**.<br />
 |_ La conf du 'reverse proxy' **nginx** qui permet d'éviter les requêtes cross-origin

## Prérequis
 - Installer Docker et Docker-Compose localement.
 - Installer Make.
 - Télécharger les données : `make download-data`

### Les micro-services

### Nginx
 -  Fabriquer l'image docker : `make nginx`. Lance le service **nginx** dans un docker. Seul le port 80 est exposé. Tester avec http://localhost

### Elasticsearch
 - Fabriquer l'image docker : `make elasticsearch`. Lance ES et crée un réseau docker.
 - Tester la base ayant une route nginx: `curl http://elasticsearch`

### Backend
 - Fabriquer l'image docker du backend : `make backend-dev`. Cela aura pour effet de lancer l'application **Flask**.
 - Rentrer dans le container : `make backend-exec`.
 - Lancer les tests unitaires, qui va indexer les données tests `pytest tests/iga`.
 - Tester le back : http://localhost/api/common/healthcheck


### Frontend
  - **Sapper** pour le routage, **Svelte** pour l'UI et **Tailwindcss** pour la mise en forme.
  - Fabriquer l'image docker du frontend : `make frontend-dev`.
  - Se rendre à http://localhost (Le hot-reloading est configuré)

### Kibana
  - Pour tester efficacement des changements de mapping dans l'index, la console dev de **Kibana** peut être utile.
  - Lancer Kibana avec `make kibana`. Le container Elasticsearch doit tourner. Se rendre à l'adresse http://localhost/5601
