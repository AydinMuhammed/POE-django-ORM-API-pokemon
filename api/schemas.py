from ninja import Field, Schema, ModelSchema
from pokemon.models import Type, Pokemon, Generation

class SumSchema(Schema):
    """Schema to sum two numbers."""
    x : float
    y : float
    
class TypeSchema(ModelSchema):
    """ Ninja schema for the Pokemon type model. """

    class Meta:
        model = Type
        fields = "__all__"

class TypeCreationSchema(ModelSchema):
    """ Ninja schema for the Pokemon type model. """

    class Meta:
        model = Type
        fields = ["name", "description"]

class GenerationSchema(ModelSchema):
    """Ninja schema for the Pokemon generation model."""

    class Meta:
        model = Generation
        fields = "__all__"

class PokemonSchema(ModelSchema):
    """
    Ninja schema for the Pokemon model.
    
    This schema serializes the Pokemon model with
    foreign key relations shown as nested objects.
    """
    type1: TypeSchema
    type2: TypeSchema | None
    generation : GenerationSchema

    class Meta:
        model = Pokemon
        fields = "__all__"

class PokemonCreateSchema(ModelSchema):
    """
    Ninja schema for the Pokemon model (input).
    
    This schema serializes the Pokemon model with
    foreign key relations shown as nested objects.
    """
    type1_name: str
    type2_name: str | None
    generation_number: int

    class Meta:
        model = Pokemon
        exclude = ["id", "type1", "type2", "generation"]

#Autre façon de faire/exemple
class PokemonSchemaMini(ModelSchema):
    """ Ninja schema for the Pokemon model

    This schema serializes the Pokemon model with the type1 field
    only serializes as string
    """
    type1_name: str = Field(..., alias="type1.name")
    
    class Meta:
        model = Pokemon
        fields = None
        exclude = ["type1"]

