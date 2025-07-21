from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import csv
import re

from pokemon.models import Generation, Pokemon, Type


class Command(BaseCommand):
    help = "Loads pokemon data from a csv file."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Executes the command.

        Load the pokemon.csv file and display column info.
        """
        path: Path = Path(__file__).parent.parent.parent.parent / "data" / "pokemon.csv"
        with path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:  
                    # Match a name starting with an uppercase letter followed by lowercase letters,
                    # optionally followed by a second part starting with an uppercase letter or digit.
                    result = re.fullmatch("^([A-Z][a-z]+)([A-Z0-9]?.*)$", row["Name"])
                    # There are two groups detected, name and version
                    name, version = result.groups()

                    # Try to get or create types for type1 and type2 (if value is not empty)
                    type1 = Type.objects.get_or_create(name=row["Type 1"])[0] if row["Type 1"] != "" else None
                    type2 = Type.objects.get_or_create(name=row["Type 2"])[0] if row["Type 2"] != "" else None
                    # Try to get or create generation object
                    generation = Generation.objects.get_or_create(number=row["Generation"])[0]

                    # Create the pokemon
                    pokemon = Pokemon.objects.create(
                        number=row["#"],
                        name=name,
                        version=version,
                        type1=type1,
                        type2=type2,
                        hp=row["HP"],
                        attack=row["Attack"],
                        defense=row["Defense"],
                        special_attack=row["Sp. Atk"],
                        special_defense=row["Sp. Def"],
                        speed=row["Speed"],
                        generation=generation,
                        legendary=row["Legendary"],
                    )