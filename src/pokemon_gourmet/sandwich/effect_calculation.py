__all__ = ["calculate_effects"]

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from pokemon_gourmet.enums import Flavor, Power
from pokemon_gourmet.sandwich.ingredient_data import ingredient_data
from pokemon_gourmet.singleton import Singleton

if TYPE_CHECKING:
    from pokemon_gourmet.sandwich.recipe import Recipe

FLAVOR_COMBO_BONUS: dict[tuple[Flavor, Flavor], Power] = {
    (Flavor.SWEET, Flavor.SALTY): Power.EGG,
    (Flavor.SWEET, Flavor.SOUR): Power.CATCHING,
    (Flavor.SWEET, Flavor.BITTER): Power.EGG,
    (Flavor.SWEET, Flavor.HOT): Power.RAID,
    (Flavor.SALTY, Flavor.SWEET): Power.ENCOUNTER,
    (Flavor.SALTY, Flavor.SOUR): Power.ENCOUNTER,
    (Flavor.SALTY, Flavor.BITTER): Power.EXP_POINT,
    (Flavor.SALTY, Flavor.HOT): Power.ENCOUNTER,
    (Flavor.SOUR, Flavor.SWEET): Power.CATCHING,
    (Flavor.SOUR, Flavor.SALTY): Power.TEENSY,
    (Flavor.SOUR, Flavor.BITTER): Power.TEENSY,
    (Flavor.SOUR, Flavor.HOT): Power.TEENSY,
    (Flavor.BITTER, Flavor.SWEET): Power.ITEM_DROP,
    (Flavor.BITTER, Flavor.SALTY): Power.EXP_POINT,
    (Flavor.BITTER, Flavor.SOUR): Power.ITEM_DROP,
    (Flavor.BITTER, Flavor.HOT): Power.ITEM_DROP,
    (Flavor.HOT, Flavor.SWEET): Power.RAID,
    (Flavor.HOT, Flavor.SALTY): Power.HUMUNGO,
    (Flavor.HOT, Flavor.SOUR): Power.HUMUNGO,
    (Flavor.HOT, Flavor.BITTER): Power.HUMUNGO,
}


class EffectCalculator(metaclass=Singleton):
    """Calculate the effects of a recipe, based on the formula derived
    by @cecilbowen.

    Check <https://github.com/cecilbowen/pokemon-sandwich-simulator>.

    Args:
        recipe: Recipe to calculate effects
    """

    def __init__(self) -> None:
        self.recipe = None
        self.bonus_mat = np.zeros((len(Flavor), len(Flavor), len(Power)), dtype=int)

        for (flavor1, flavor2), power in FLAVOR_COMBO_BONUS.items():
            i = flavor1.value - 1
            j = flavor2.value - 1
            k = power.value - 1
            self.bonus_mat[i, j, k] = 100

    def __call__(self, recipe: "Recipe") -> NDArray[np.intp]:
        self.recipe = recipe
        return self.compute_effects()

    def compute_effects(self) -> NDArray[np.intp]:
        """Compute the effects of a recipe.

        Returns:
            List of tuples containing a Power, a Pokémon Type, and a Level.
        """
        if self.recipe is None:
            raise ValueError()
        ingredient_counts = self.recipe._ingredient_list * ingredient_data.pieces

        flavor_sum = ingredient_counts @ ingredient_data.flavor_mat
        i, j = np.argsort(-1 * flavor_sum, kind="stable").tolist()[:2]

        power_sum = ingredient_counts @ ingredient_data.power_mat
        power_sum += self.bonus_mat[i, j, :]

        # Force Sparkling Power to zero if there are less than two Herba Mystica
        not_sparkling = np.arange(len(Power)) != (Power.SPARKLING.value - 1)
        power_sum *= not_sparkling | (power_sum >= 2000)

        power_ids = np.argsort(-1 * power_sum, kind="stable")[:3]

        type_sum = ingredient_counts @ ingredient_data.type_mat
        types_ids = np.argsort(-1 * type_sum, kind="stable")[:3]
        type_values = type_sum[types_ids]

        sorted_types = np.take(types_ids, self.sort_types(type_values))
        levels = self.compute_levels(type_values)

        return np.column_stack([power_ids, sorted_types, levels])

    @staticmethod
    def sort_types(values: NDArray) -> tuple[int, int, int]:
        """Return the indices that would sort the Type array.

        Returns:
            Tuple of indices that sort the Type array.
        """
        assert len(values) == 3
        difference = values[0] - values[1]

        if values[0] > 480:
            return (0, 0, 0)
        elif values[0] > 280:
            return (0, 0, 2)
        else:
            split = False
            if values[0] > 105 and difference > 105:
                return (0, 0, 2)
            elif 100 <= values[0] <= 105:
                split = difference >= 80 and values[1] <= 21
            elif 90 <= values[0] < 100:
                split = difference >= 78 and values[1] <= 16
            elif 80 <= values[0] < 90:
                split = difference >= 74 and values[1] <= 9
            elif 74 <= values[0] < 80:
                split = difference >= 72 and values[1] <= 5
            if split:
                return (0, 2, 0)
            return (0, 2, 1)

    @staticmethod
    def compute_levels(values: NDArray) -> tuple[int, int, int]:
        """Calculate the Levels of each effect.

        Returns:
            Three Levels associated with each recipe effect
        """
        if values[0] < 180:
            return (1, 1, 1)
        elif values[0] <= 280:
            if values[1] >= 180 and values[2] >= 180:
                return (2, 2, 1)
            else:
                return (2, 1, 1)
        elif values[0] < 380:
            if values[2] >= 180:
                return (2, 2, 2)
            else:
                return (2, 2, 1)
        elif values[0] < 460:
            if values[1] >= 380 and values[2] >= 380:
                return (3, 3, 3)
            else:
                return (3, 3, 2)
        else:
            return (3, 3, 3)


calculate_effects = EffectCalculator()
