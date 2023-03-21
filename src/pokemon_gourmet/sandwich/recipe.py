__all__ = ["Recipe"]

from collections.abc import Collection, Hashable, Iterator
from typing import cast

from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.effect_calculation import calculate_effects
from pokemon_gourmet.sandwich.ingredient import Condiment, Filling, Ingredient
from pokemon_gourmet.sandwich.ingredient_data import INGREDIENTS

RecipeTuple = tuple[str, ...]


class Recipe(Collection, Hashable):
    """A collection of condiments and fillings"""

    def __init__(self, condiments: list[Condiment], fillings: list[Filling]) -> None:
        self.condiments = condiments
        self.fillings = fillings
        self._effects = None

    @classmethod
    def from_str(cls, *ingredient_names: str) -> "Recipe":
        ingredients = ([], [])
        for name in ingredient_names:
            ingredient = INGREDIENTS[name]
            ingredients[ingredient.is_filling].append(ingredient)
        recipe = cls(*ingredients)
        if recipe.is_legal:
            return recipe
        raise ValueError("Recipe is not legal.")

    @property
    def effects(self) -> EffectList:
        if self._effects is None:
            self._effects = calculate_effects(self)
        return EffectList(self._effects)

    @property
    def ingredients(self) -> list[Ingredient]:
        return self.condiments + self.fillings

    @property
    def is_legal(self) -> bool:
        return 0 < len(self.fillings) <= 6 and 0 < len(self.condiments) <= 4

    @property
    def has_herba_mystica(self) -> bool:
        return any(condiment.is_herba_mystica for condiment in self.condiments)

    @property
    def herba_mystica_count(self) -> int:
        count = 0
        for condiment in self.condiments:
            if condiment.is_herba_mystica:
                count += 1
        return count

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """Add ingredient to recipe and reset its effects."""
        self._effects = None  # Reset effects
        if ingredient.is_condiment:
            self.condiments.append(cast(Condiment, ingredient))
        else:
            self.fillings.append(cast(Filling, ingredient))

    def astuple(self) -> RecipeTuple:
        """Return the sorted list of ingredients as a tuple."""
        return tuple([ingredient.name for ingredient in sorted(self.ingredients)])

    def __contains__(self, ingredient: Ingredient) -> bool:
        if ingredient.is_condiment:
            return ingredient in self.condiments
        return ingredient in self.fillings

    def __eq__(self, other: "Recipe") -> bool:
        return self.__class__ == other.__class__ and self.astuple() == other.astuple()

    def __hash__(self) -> int:
        return hash(self.astuple())

    def __iter__(self) -> Iterator[Ingredient]:
        return iter(self.ingredients)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __repr__(self) -> str:
        s = "s" if len(self.ingredients) != 1 else ""
        return f"Recipe({len(self.ingredients)} ingredient{s})"

    def __str__(self) -> str:
        if len(self.ingredients) > 0:
            return "Recipe Effects:\n" + "\n".join(map(str, self.effects))
        return "Empty Recipe"
