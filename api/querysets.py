from typing import Any
from django.db import IntegrityError
from api.schemas import PokemonSchema, PokemonSchemaMini, TypeCreationSchema, TypeSchema, PokemonCreateSchema
from pokemon.models import Pokemon, Type, Generation
from .ninja import api
from ninja.pagination import paginate, PageNumberPagination

# Pour tester dans Postman, il faut faire un GET sur http://127.0.0.1:8000/api/pokemons
@api.get("/pokemons", response = list[PokemonSchemaMini])
@paginate(PageNumberPagination, page_size=10)
def list_pokemons(request):
    pokemons = Pokemon.objects.all()
    return pokemons

# Pour tester dans Postman, il faut faire un POST sur http://127.0.0.1:8000/api/type/create
@api.post("/type/create", response=TypeSchema)
def create_type(request, type: TypeCreationSchema):
    # Créer ou mettre à jour les informations d'un Type
    # avec la méthode `objects.update_or_create` :
    # ici, l'argument name= indique qu'on cherche en premier lieu
    # un objet avec une valeur précise à l'attribut name
    # l'argument defaults= permet d'indiquer que, si on trouve cet objet
    # on mettra à jour son attribut description=
    instance, updated = Type.objects.update_or_create(name=type.name, defaults={"description": type.description})
    return instance

 # Récupérer la liste complète des types existants.
 # Pour tester dans Postman, il faut faire un GET sur http://127.0.0.1:8000/api/types
@api.get("/types", response=list[TypeSchema])
def list_types(request):
    """
    Route to list all types.
    
    Returns:
        list[TypeSchema]: A list of all types.
    """
    types = Type.objects.all()
    return types

# Récupérer les détails d’un type à partir de son nom.
# Pour tester dans Postman, il faut faire un GET sur http://127.0.0.1:8000/api/type/{name}
# Exemple : http://127.0.0.1:8000/api/type/Steel
@api.get("/type/{name}", response=TypeSchema)
def get_type(request, name: str):
    """
    Route to get a type by its name.
    
    Args:
        request (Request): The request object.
        name (str): The name of the type.
    
    Returns:
        TypeSchema: The type object.
    """
    type = Type.objects.get(name=name)
    return type

# Créer un Pokémon.
# Pour tester dans Postman, il faut faire un POST sur http://127.0.0.1:8000/api/pokemon/create
# Exemple de json à envoyer pour ce post :
# {
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
# }
@api.post("/pokemon/create", response={200: PokemonSchema, 401: Any})
def create_pokemon(request, pokemon: PokemonCreateSchema):
    """
    Route to create a pokemon.
    
    Uses a custom schema to create the pokemon.
    The schema does not include the type1 and type2 fields, as these are foreign keys to the Type model.
    It does not include the generation field, as this is a foreign key to the Generation model.
    Instead it includes the type1_name, type2_name and generation_number fields, which are used to look up the type and generation objects.

    Once it's done, we create a new Pokemon object an set its attributes from
    the input pokemon object (as a dict), the we set the foreign keys on the instance.

    If an error occurs, it returns a 401 status code and a message.
    See https://django-ninja.dev/guides/response/#multiple-response-schemas

    Args:
        request (Request): The request object.
        pokemon (PokemonCreateSchema): The pokemon to create.
    
    Returns:
        Pokemon: The created pokemon.
    """
    try:
        type1 = Type.objects.get(name=pokemon.type1_name)
        type2 = Type.objects.get(name=pokemon.type2_name) if pokemon.type2_name is not None else None
        generation = Generation.objects.get(number=pokemon.generation_number)
        instance = Pokemon()
        for attr, value in pokemon.dict().items():
            setattr(instance, attr, value)
        # Define foreign keys on the instance
        instance.type1 = type1
        instance.type2 = type2
        instance.generation = generation
        instance.save()
    except IntegrityError:
        return (401, {"detail": "Pokemon cannot be created, it already exists."})
    return instance
