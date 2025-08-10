# HTTP Request Plugin for Home Assistant

Permet d'envoyer des requêtes HTTP simples définies dans un fichier `requests.yaml`.

## Installation

1. Copier le dossier `http_request_plugin` dans `config/custom_components/`
2. Créer `requests.yaml` dans le dossier du plugin, exemple :
    ```yaml
    requete1:
      url: "https://api.example.com/do-action"
      nom: "Action 1"
    ```
3. Redémarrer Home Assistant.

## Utilisation

- Appeler le service `http_request_plugin.send_request` dans Outils développeur > Services :
    ```yaml
    nom: "requete1"
    ```
- La réponse sera envoyée sur le bus d'événements Home Assistant (`http_request_plugin.response`).

## Pour HACS

- Publier ce dossier sur GitHub, puis l’ajouter à HACS comme custom repository.

---

**Pour aller plus loin :**
- Supporte uniquement GET, mais tu peux ajouter POST, headers, payload.
- Pour afficher la réponse dans Home Assistant, utilise une automation sur l’événement `http_request_plugin.response`.
