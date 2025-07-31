from ninja import Path, Router
from api.schemas import SumSchema

# Création d'un routeur Ninja pour les routes de base de l'API.
router = Router()

@router.get("/")
# Endpoint d'accueil de l'API.
# Système de routing : cette route correspond à /api/basics/ (voir api/ninja.py).
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/basics/
def welcome(request, a: int | float = 1, b: int = 2):
    """
    Basic entry point for the API.

    Returns:
        dict: A message indicating the API is **up and running**.
    """
    return {"message": f"Welcome to Pokémon API {a + b}"}

@router.get("/users/{id}")
# Endpoint dynamique pour afficher un message avec l'id utilisateur.
# Système de routing : cette route correspond à /api/basics/users/{id}
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/basics/users/1
# Remplacez 1 par l'id souhaité.
def user_detail(request, id: int):
    """
    Entry point with dynamic part for the API.

    Args:
        id (int): The id of the user

    Returns:
        dict: A message indicating the API is **up and running**.
    """
    return {"message": f"Welcome to Pokémon API {id}"}

@router.post("/sum")
# Endpoint pour additionner deux nombres envoyés en JSON.
# Système de routing : cette route correspond à /api/basics/sum
# Pour tester dans Postman :
# - Méthode : POST
# - URL : http://127.0.0.1:8000/api/basics/sum
# - Body (JSON) :
#   {
#     "x": 5,
#     "y": 7
#   }
def sum_numbers(request, pair: SumSchema):
    return {"result": pair.x + pair.y}

@router.get("/sum2/{x}/{y}")
# Endpoint pour additionner deux nombres passés dans l'URL.
# Système de routing : cette route correspond à /api/basics/sum2/{x}/{y}
# Pour tester dans Postman :
# - Méthode : GET
# - URL : http://127.0.0.1:8000/api/basics/sum2/1/2
# Remplacez 1 et 2 par les valeurs souhaitées.
def sum_numbers2(request, pair: Path[SumSchema]):
    """
    Entry point with dynamic part and path parameters for the API.

    The `pair` argument is detected from the URL.
    The dynamic parts `x` and `y` are detected from the URL and
    used to set the attributes `x` and `y` of the `SumSchema` object.

    Args:
        x (int | float): The first number to be added
        y (int | float): The second number to be added

    Returns:
        dict: A message indicating the API is **up and running**.
    """
    return {"result": pair.x + pair.y}

# Explications générales :
# - Le système de routing de Django Ninja permet de définir des routes statiques ou dynamiques (avec des paramètres dans l'URL).
# - Les routes de ce fichier sont accessibles sous le préfixe /api/basics/ grâce à l'ajout du routeur dans api/ninja.py.
# - Pour tester chaque endpoint dans Postman, il faut bien respecter la méthode HTTP, l'URL, et fournir les bons paramètres (dans l'URL ou en JSON).