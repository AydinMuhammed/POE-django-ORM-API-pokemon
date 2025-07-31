"""API routes for Pokemon instances."""

from typing import Any
from api.schemas import PokemonSchema, TypeSchema
from ninja import Router
from ninja_apikey.security import APIKeyAuth

from pokemon.models import Type, Pokemon
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

# Création d'un routeur Ninja avec authentification par clé API par défaut.
# Toutes les routes définies dans ce fichier nécessitent la présence d'un header X-API-KEY valide,
# sauf si un autre système d'authentification est précisé sur une route spécifique.
router = Router(auth=APIKeyAuth())

@router.get("view/{number}", response={200: PokemonSchema, 404: Any})
# Endpoint pour récupérer un Pokémon par son numéro et sa version.
# Système de routing : l'URL attend un paramètre dynamique {number}.
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/pokemon/view/{number}
# - Header : X-API-KEY : <votre_clé_api>
# Remplacez {number} par le numéro du Pokémon recherché.
def pokemon_view(request, number: int, version: str = ""):
    """Détaille un Pokémon selon son numéro et sa version."""
    try:
        return Pokemon.objects.get(number=number, version=version)
    except Pokemon.DoesNotExist:
        return (404, {"message": "Pokemon not found"})

@router.get("view-all/{number}", response={200: list[PokemonSchema], 404: Any}, auth=HttpJwtAuth())
# Endpoint pour récupérer tous les Pokémon ayant un certain numéro (toutes versions confondues).
# Système de routing : l'URL attend un paramètre dynamique {number}.
# Cette route utilise l'authentification JWT (token Bearer) au lieu de la clé API.
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/pokemon/view-all/{number}
# - Header : Authorization : Bearer <votre_token_jwt>
# Remplacez {number} par le numéro du Pokémon recherché.
def pokemon_view_all(request, number: int):
    """Détaille tous les Pokémon d'un numéro donné (toutes versions)."""
    print(request.user.username)
    pokemons = Pokemon.objects.filter(number=number)
    if pokemons.count() == 0:
        return (404, {"message": "Pokemon not found"})
    else:
        return pokemons

# Explications générales :
# - Le système de routing de Django Ninja permet de définir des routes dynamiques avec des paramètres dans l'URL (ex: {number}).
# - L'authentification peut être définie globalement pour toutes les routes du fichier (ici, clé API) ou individuellement pour une route (ici, JWT).
# - Pour tester chaque endpoint dans Postman, il faut bien respecter la méthode HTTP, l'URL, et fournir le bon header d'authentification selon la