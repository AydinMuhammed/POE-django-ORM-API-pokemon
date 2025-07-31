from ninja import Router
from ninja.security import HttpBasicAuth
from django.contrib.auth import authenticate
from ninja_apikey.security import APIKeyAuth

# Création d'un routeur Ninja sans authentification globale.
# Chaque route peut définir son propre système d'authentification.
router = Router()

class FakeBasicAuth(HttpBasicAuth):
    """
    Classe d'authentification basique personnalisée.
    Vérifie les identifiants (username/password) dans la base de données Django.
    Si les identifiants sont valides, retourne l'utilisateur ; sinon, retourne None.
    """
    def authenticate(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            return user
        return None

@router.get("basic", auth=FakeBasicAuth())
# Endpoint protégé par authentification Basic.
# Système de routing : l'URL attend /api/auth/basic (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/auth/basic
# - Auth : Basic Auth (renseigner username et password d'un utilisateur Django)
def basic_auth_protection(request):
    """Vérifie si l'utilisateur est authentifié via Basic Auth."""
    return {"message": f"Your are authenticated as {request.auth}"}

@router.get("key", auth=APIKeyAuth())
# Endpoint protégé par authentification par clé API.
# Système de routing : l'URL attend /api/auth/key (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/auth/key
# - Header : X-API-KEY : <votre_clé_api>
def api_key_protection(request):
    """
    Vérifie si l'utilisateur est authentifié via une clé API.
    La clé API doit être transmise dans le header X-API-KEY.
    """
    return {"message": f"Your are authenticated with API key {request.auth}"}

# Explications générales :
# - Le système de routing de Django Ninja permet de définir des routes accessibles via /api/auth/basic et /api/auth/key.
# - Chaque route peut avoir son propre système d'authentification (ici Basic ou API Key).
# - Pour tester dans Postman, il faut bien utiliser la bonne méthode HTTP, l'URL, et fournir les bons identifiants ou headers selon la