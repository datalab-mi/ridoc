_Dépot boite à outils pour un mote._

## Présentation
 Makefile : Contient les commandes et variables du projet.<br />
 |_ elasticsearch : Fichiers de config pour *ElasticSearch*.<br />
 |_ backend : Serveur *Flask* et indexation de la base ouverte pour tester. [bonnes feuilles](https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles).<br />
 |_ frontend : Code source pour distribuer une interface utilisateur branché à ElasticSearch. Fourni un site statique en *React*.<br />


## Prérequis
 - Installer Docker et Docker-Compose localement.
 - Installer Make.
 - Télécharger les données : `make download-data`

### Elasticsearch
 - Fabriquer l'image docker : `make elasticsearch`. Lance ES et crée un réseau docker.
 - Tester la base : `curl http://localhost:9200`

### Backend

 - Fabriquer l'image docker du backend : `make backend-dev`. Cela aura pour effet de lancer l'application Flask.
 - Rentrer dans le container : `make backend-exec`.
 - Lancer les tests unitaires, qui va indexer les données tests `pytest tests/iga`.

### Frontend

  - Fabriquer l'image docker du frontend : `make frontend-dev`.
  - Se rendre à curl http://localhost:3000
