__all__ = ["Recipe"]

from collections.abc import Collection, Hashable, Iterator
from typing import Union, cast

import numpy as np

from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.effect_calculation import calculate_effects
from pokemon_gourmet.sandwich.ingredient_data import ingredient_data

MAX_CONDIMENTS = 4
MAX_FILLINGS = 6
MAX_PLAYERS = 4

RecipeTuple = tuple[int, ...]
Ingredient = Union[int, str]


class Recipe(Collection, Hashable):
    """A collection of condiments and fillings"""

    def __init__(self, *ingredients: Ingredient, num_players: int = 1) -> None:
        self.num_players = max(min(num_players, MAX_PLAYERS), 1)
        self._effects = None
        self._ingredient_list = np.zeros(len(ingredient_data), dtype=int)
        for ingredient in ingredients:
            i = self._get_ingredient_index(ingredient)
            self._ingredient_list[i] += 1

    def __contains__(self, ingredient: Ingredient) -> bool:
        i = self._get_ingredient_index(ingredient)
        return self._ingredient_list[i] > 0

    def __eq__(self, other: "Recipe") -> bool:
        return self.__class__ == other.__class__ and cast(
            bool, np.all(self._ingredient_list == other._ingredient_list)
        )

    def __hash__(self) -> int:
        return hash(self.astuple())

    def __iter__(self) -> Iterator[Ingredient]:
        return iter(self.ingredients)

    def __len__(self) -> int:
        return self._ingredient_list.sum()

    def __repr__(self) -> str:
        s = "s" if len(self) != 1 else ""
        return f"Recipe({len(self)} ingredient{s})"

    def __str__(self) -> str:
        if len(self.ingredients) > 0:
            return "Recipe Effects:\n" + "\n".join(map(str, self.effects))
        return "Empty Recipe"

    @property
    def effects(self) -> EffectList:
        if self._effects is None:
            self._effects = calculate_effects(self)
        return EffectList(self._effects)

    @property
    def condiments(self) -> list[str]:
        ids = np.flatnonzero(self._ingredient_list * ingredient_data.is_condiment)
        counts = np.take(self._ingredient_list, ids).tolist()
        return [
            ingredient_data[i] for i, count in zip(ids, counts) for _ in range(count)
        ]

    @property
    def fillings(self) -> list[str]:
        ids = np.flatnonzero(self._ingredient_list * ingredient_data.is_filling)
        counts = np.take(self._ingredient_list, ids).tolist()
        return [
            ingredient_data[i] for i, count in zip(ids, counts) for _ in range(count)
        ]

    @property
    def ingredients(self) -> list[str]:
        ids = np.flatnonzero(self._ingredient_list)
        counts = np.take(self._ingredient_list, ids).tolist()
        return [
            ingredient_data[i] for i, count in zip(ids, counts) for _ in range(count)
        ]

    @property
    def is_legal(self) -> bool:
        ingredient_counts = self._ingredient_list * ingredient_data.pieces
        ingredient_limit = np.all(
            ingredient_data.is_condiment
            | (ingredient_counts <= self.single_ingredient_limit)
        )
        return (
            1 <= (self.num_fillings / self.num_players) <= MAX_FILLINGS
            and 1 <= (self.num_condiments / self.num_players) <= MAX_CONDIMENTS
            and cast(bool, ingredient_limit)
        )

    @property
    def num_condiments(self) -> int:
        return self._ingredient_list[ingredient_data.is_condiment].sum()

    @property
    def num_fillings(self) -> int:
        return self._ingredient_list[ingredient_data.is_filling].sum()

    @property
    def total_pieces(self) -> int:
        counts = self._ingredient_list * ingredient_data.pieces
        return counts[ingredient_data.is_filling].sum()

    @property
    def num_herba_mystica(self) -> int:
        return self._ingredient_list[ingredient_data.is_herba_mystica].sum()

    @property
    def single_ingredient_limit(self) -> int:
        return 15 if self.num_players > 1 else 12

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """Add ingredient to recipe and reset its effects."""
        self._effects = None  # Reset effects
        i = self._get_ingredient_index(ingredient)
        self._ingredient_list[i] += 1

    def astuple(self) -> RecipeTuple:
        """Return the list of ingredient indices as a tuple."""
        return tuple(self._ingredient_list.tolist())

    def count(self, ingredient: Ingredient) -> int:
        """Return the count of the given ingredient."""
        i = self._get_ingredient_index(ingredient)
        return cast(int, self._ingredient_list[i])

    @staticmethod
    def _get_ingredient_index(ingredient: Ingredient) -> int:
        if isinstance(ingredient, str):
            return ingredient_data.index(ingredient)
        return ingredient
