from django.contrib import admin
from pokemon.models import Generation, Pokemon, Type
# Register your models here.
# Enregistrer les modèles pour qu'ils soient accessibles dans l'interface d'administration

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Admin configuration for Type model."""
    list_display = ("pk", "name", "description")


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    """Admin configuration for Generation model."""
    list_display = ("pk", "number", "description")


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    """Admin configuration for Pokemon model."""
    list_display = ("pk", "number", "name", "version", "type1", "type2", "hp", "attack", "defense", "special_attack", "special_defense", "speed", "generation", "legendary")
    list_filter = ("type1","type2","generation","legendary")
    search_fields = ("name", "version")