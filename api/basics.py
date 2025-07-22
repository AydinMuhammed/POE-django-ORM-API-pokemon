from ninja import NinjaAPI, Path
from .schemas import SumSchema

api = NinjaAPI(title="Pokémon API")
@api.get("/")
def welcome(request, a : int | float = 1, b : int | float = 1):
    """
    Basic entry point for the API.

    Returns:
        dict: A message indicating the API is working.
    """
    return {"message": f"Welcome to the Pokémon API {a + b}"}

@api.get("/users/{id}")
def user_details(request, id : int):
    """
    Entry point with dynamic part for the API.

    Args:
        id (int): The user ID.

    Returns:
        dict: A message indicating the API is working.
    """
    return {"message": f"Welcome to the Pokémon API {id}"}

@api.post("/sum")
def sum_numbers(request, pair: SumSchema):
    return {"result": pair.x + pair.y}

@api.get("/sum2/{x}/{y}")
def sum_numbers2(request, pair: Path[SumSchema]):
    """
    Entry point <ith dynamic part and path parameters for the API.

    The 'pair' 
    The dynamic
    """

    return {"result": pair.x + pair.y}