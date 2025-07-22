from api.schemas import PokemonSchema
from pokemon.models import Pokemon
from .ninja import api

@api.get("/pokemons", response = list[PokemonSchema])
def list_pokemons(request):
    pokemons = Pokemon.objects.all()
    return pokemons