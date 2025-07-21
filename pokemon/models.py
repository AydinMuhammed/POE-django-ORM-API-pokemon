from django.db import models



class Type(models.Model):
    """Pokémon type."""
    name = models.CharField(max_length=64, unique=True, verbose_name="name")
    description = models.TextField(blank=True, verbose_name="description")

    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"
        ordering = ["name"]
        
    
    def __str__(self):
        return self.name


class Generation(models.Model):
    """Pokémon game generation."""
    number = models.PositiveSmallIntegerField(unique=True, verbose_name="number")
    description = models.TextField(blank=True, verbose_name="description")

    class Meta:
        verbose_name = "generation"
        verbose_name_plural = "generations"
        ordering = ["number"]
        
    def __str__(self):
        return f"Generation {self.number}"


class Pokemon(models.Model):
    """Pokémon information."""
    number = models.PositiveSmallIntegerField(verbose_name="number")
    name = models.CharField(max_length=64, verbose_name="name")
    version = models.CharField(max_length=64, verbose_name="version")
    type1 = models.ForeignKey("pokemon.Type", on_delete=models.PROTECT, related_name="pokemon_type1", verbose_name="type 1")
    type2 = models.ForeignKey("pokemon.Type", on_delete=models.PROTECT, null=True, related_name="pokemon_type2", verbose_name="type 2")
    hp = models.PositiveSmallIntegerField(verbose_name="hp")
    attack = models.PositiveSmallIntegerField(verbose_name="attack")
    defense = models.PositiveSmallIntegerField(verbose_name="defense")
    special_attack = models.PositiveSmallIntegerField(verbose_name="special attack")
    special_defense = models.PositiveSmallIntegerField(verbose_name="special defense")
    speed = models.PositiveSmallIntegerField(verbose_name="speed")
    generation = models.ForeignKey("pokemon.Generation", on_delete=models.PROTECT, verbose_name="generation")
    legendary = models.BooleanField(default=False, verbose_name="legendary")

    class Meta:
        verbose_name = "pokémon"
        verbose_name_plural = "pokémons"
        unique_together = [("number", "name", "version")]
        

    def __str__(self):
        return f"{self.name} ({self.version})"