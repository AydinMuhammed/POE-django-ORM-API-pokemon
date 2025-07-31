from typing import Any
from django.db import IntegrityError
from api.schemas import PokemonSchema, PokemonSchemaMini, TypeCreationSchema, TypeSchema, PokemonCreateSchema
from pokemon.models import Pokemon, Type, Generation
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination

# Création d'un routeur Ninja pour les opérations sur les ensembles de données (querysets).
router = Router()

@router.get("/pokemons", response = list[PokemonSchemaMini])
@paginate(PageNumberPagination, page_size=10)
# Endpoint pour lister tous les Pokémons avec pagination.
# Système de routing : cette route correspond à /api/querysets/pokemons (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/querysets/pokemons
# - Paramètres de pagination possibles : ?page=1
def list_pokemons(request):
    """List all Pokemons."""
    pokemons = Pokemon.objects.all()
    return pokemons

@router.post("/pokemon/create", response={200: PokemonSchema, 401: Any})
# Endpoint pour créer un nouveau Pokémon.
# Système de routing : cette route correspond à /api/querysets/pokemon/create (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : POST
# - URL : http://127.0.0.1:8000/api/querysets/pokemon/create
# - Body (JSON) :
#   {
#     "number": 991,
#     "name": "Boulbizarre",
#     "version": "Domotique",
#     "type1_name": "Grass",
#     "type2_name": "Poison",
#     "hp": 45,
#     "attack": 49,
#     "defense": 49,
#     "special_attack": 65,
#     "special_defense": 65,
#     "speed": 45,
#     "generation_number": 4,
#     "legendary": false
#   }
def create_pokemon(request, pokemon: PokemonCreateSchema):
    """
    Route to create a pokemon.

    Utilise un schéma personnalisé pour créer le Pokémon.
    Les champs type1 et type2 (foreign keys) sont remplacés par type1_name et type2_name,
    et la génération par generation_number, pour simplifier l'entrée côté client.

    Si une erreur survient (doublon, type ou génération inexistante), la route retourne un code 401 avec un message d'erreur.
    Voir https://django-ninja.dev/guides/response/#multiple-response-schemas

    Args:
        request (Request): L'objet requête.
        pokemon (PokemonCreateSchema): Les données du Pokémon à créer.

    Returns:
        Pokemon: Le Pokémon créé (code 200).
        401: Si le Pokémon ne peut pas être créé, ou si le type/génération n'existe pas.
    """
    try:
        type1 = Type.objects.get(name=pokemon.type1_name)
        type2 = Type.objects.get(name=pokemon.type2_name) if pokemon.type2_name is not None else None
        generation = Generation.objects.get(number=pokemon.generation_number)
        instance = Pokemon()
        for attr, value in pokemon.dict().items():
            setattr(instance, attr, value)
        # Définir les clés étrangères sur l'instance
        instance.type1 = type1
        instance.type2 = type2
        instance.generation = generation
        instance.save()
    except IntegrityError:
        return (401, {"detail": "Pokemon cannot be created, it already exists."})
    except Generation.DoesNotExist:
        return (401, {"detail": "Generation does not exist."})
    except Type.DoesNotExist:
        return (401, {"detail": "Type does not exist."})
    return instance

# Explications générales :
# - Le système de routing de Django Ninja permet de définir des routes accessibles sous /api/querysets/ grâce à l'ajout du routeur dans api/ninja.py.
# - Les routes peuvent être statiques ou dynamiques, et acceptent des paramètres dans l'URL ou dans le corps de la requête (JSON).
# - Pour tester chaque endpoint dans Postman, il faut respecter la méthode HTTP, l'URL, et fournir les bons paramètres (dans l'URL, en query string ou en JSON).