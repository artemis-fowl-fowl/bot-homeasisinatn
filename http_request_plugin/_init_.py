"""Plugin Home Assistant pour envoyer des requêtes HTTP définies dans un fichier."""

import logging
import os
import yaml

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    path = os.path.join(hass.config.path("custom_components"), "http_request_plugin", "requests.yaml")
    if not os.path.exists(path):
        _LOGGER.warning("Fichier requests.yaml non trouvé : %s", path)
        hass.data["http_request_plugin.requests"] = {}
    else:
        with open(path, "r") as f:
            hass.data["http_request_plugin.requests"] = yaml.safe_load(f)

    async def handle_send_request(call):
        req_name = call.data.get("nom")
        reqs = hass.data["http_request_plugin.requests"]
        if reqs and req_name in reqs:
            url = reqs[req_name]["url"]
            nom_affiche = reqs[req_name].get("nom", req_name)
            _LOGGER.info(f"Envoi requête {nom_affiche} vers {url}")
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        result = await resp.text()
                hass.bus.fire("http_request_plugin.response", {
                    "nom": nom_affiche,
                    "result": result,
                    "status": resp.status,
                })
            except Exception as e:
                _LOGGER.error(f"Erreur requête {nom_affiche}: {e}")
                hass.bus.fire("http_request_plugin.response", {
                    "nom": nom_affiche,
                    "error": str(e),
                })
        else:
            _LOGGER.error(f"Requête '{req_name}' non trouvée.")
            hass.bus.fire("http_request_plugin.response", {
                "nom": req_name,
                "error": "Requête non trouvée",
            })

    hass.services.async_register("http_request_plugin", "send_request", handle_send_request)
    return True