from ninja import Schema

class SumSchema(Schema):
    """Schema to sum two numbers."""
    x : float
    y : float
