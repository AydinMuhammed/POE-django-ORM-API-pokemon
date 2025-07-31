"""API routes for Pokemon types."""

from typing import Any
from api.schemas import TypeSchema
from ninja import Router
from pokemon.models import Type

# Création d'un routeur Ninja pour les types de Pokémon.
router = Router()

@router.get("list", response=list[TypeSchema])
# Endpoint pour récupérer la liste complète des types existants.
# Système de routing : cette route correspond à /api/type/list (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/type/list
def type_list(request):
    """Liste tous les types de Pokémon."""
    types = Type.objects.all()
    return types

@router.get("view/{name}", response={200: TypeSchema, 404: dict[str, str]})
# Endpoint pour récupérer les détails d’un type à partir de son nom.
# Système de routing : cette route correspond à /api/type/view/{name}
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/type/view/Steel
# Remplacez "Steel" par le nom du type recherché.
def type_view(request, name: str):
    """
    Route pour obtenir un type par son nom.
    """
    try:
        type = Type.objects.get(name=name)
        return type
    except Type.DoesNotExist:
        return (404, {"message": "Type not found"})

@router.post("create", response=dict[str, bool | TypeSchema])
# Endpoint pour créer ou mettre à jour un type.
# Système de routing : cette route correspond à /api/type/create
# Pour tester dans Postman :
# - Méthode : POST
# - URL : http://127.0.0.1:8000/api/type/create
# - Body (JSON) :
#   {
#     "name": "Steel",
#     "description": "Steel type Pokémon are known for their high defense and resistance to many types of attacks."
#   }
def type_create(request, data: TypeSchema):
    """
    Crée ou met à jour les informations d'un Type.
    Utilise update_or_create pour créer le type si inexistant, ou mettre à jour la description sinon.
    Retourne un booléen 'created' et l'instance du type.
    """
    instance, created = Type.objects.update_or_create(name=data.name, defaults={"description": data.description})
    return {"created": created, "instance": instance}

@router.put("edit/{name}", response={200: TypeSchema, 404: Any})
# Endpoint pour modifier un type existant à partir de son nom.
# Système de routing : cette route correspond à /api/type/edit/{name}
# Pour tester dans Postman :
# - Méthode : PUT
# - URL : http://127.0.0.1:8000/api/type/edit/Steel
# - Body (JSON) :
#   {
#     "name": "Steel",
#     "description": "Nouvelle description"
#   }
# Remplacez "Steel" par le nom du type à modifier.
def type_edit(request, name: str, data: TypeSchema):
    """
    Modifie un type existant par son nom.
    Retourne le type modifié ou une erreur 404 si le type n'existe pas.
    """
    try:
        instance = Type.objects.get(name=name)
        for attr, value in data.dict().items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    except Type.DoesNotExist:
        return (404, {"message": "Type not found"})

@router.delete("delete/{name}", response=dict[str, str])
# Endpoint pour supprimer un type par son nom.
# Système de routing : cette route correspond à /api/type/delete/{name}
# Pour tester dans Postman :
# - Méthode : DELETE
# - URL : http://127.0.0.1:8000/api/type/delete/Steel
# Remplacez "Steel" par le nom du type à supprimer.
def type_delete(request, name: str):
    """
    Supprime un type par son nom.
    Retourne un message indiquant le statut de la suppression.
    """
    count, _ = Type.objects.filter(name=name).delete()
    return {"message": "Type deleted" if count else "Type not found"}

# Explications générales :
# - Le système de routing de Django Ninja permet de définir des routes accessibles sous /api/type/ grâce à l'ajout du routeur dans api/ninja.py.
# - Les routes peuvent être statiques ou dynamiques, et acceptent des paramètres dans l'URL ou dans le corps de la requête (JSON).
# - Pour tester chaque endpoint dans Postman, il faut respecter la méthode HTTP, l'URL, et fournir les bons paramètres (dans l'URL ou en JSON).