__all__ = ["calculate_effects"]

from collections import defaultdict
from typing import TYPE_CHECKING, Literal, TypeVar, Union, overload

from pokemon_gourmet.enums import Flavor, Power, Type, _Attribute
from pokemon_gourmet.sandwich.effect import EffectTuple
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

AttributeDict = Union[dict[Flavor, int], dict[Power, int], dict[Type, int]]
AttributeName = Literal["flavor", "power", "pokemon_type", "type"]
AttributeT = TypeVar("AttributeT", bound=_Attribute)


class EffectCalculator(metaclass=Singleton):
    """Calculate the effects of a recipe, based on the formula derived
    by @cecilbowen.

    Check <https://github.com/cecilbowen/pokemon-sandwich-simulator>.

    Args:
        recipe: Recipe to calculate effects
    """

    def __init__(self) -> None:
        self.recipe = None

    def __call__(self, recipe: "Recipe") -> list[EffectTuple]:
        self.recipe = recipe
        self.dominant_types: list[Type] = []
        self.dominant_type_values: list[int] = []
        return self.compute_effects()

    @staticmethod
    def sort_key(attr_sum: tuple[AttributeT, int]) -> tuple[int, int]:
        return (attr_sum[1], -attr_sum[0].value)

    @staticmethod
    def sort_attr_sum(attr_sum: dict[AttributeT, int]) -> dict[AttributeT, int]:
        sorted_attr_sum = sorted(
            attr_sum.items(), key=EffectCalculator.sort_key, reverse=True
        )
        return dict(sorted_attr_sum)

    @overload
    def get_attr_sum(self, attr_name: Literal["flavor"]) -> dict[Flavor, int]:
        ...

    @overload
    def get_attr_sum(self, attr_name: Literal["power"]) -> dict[Power, int]:
        ...

    @overload
    def get_attr_sum(
        self, attr_name: Literal["pokemon_type", "type"]
    ) -> dict[Type, int]:
        ...

    def get_attr_sum(self, attr_name: AttributeName) -> AttributeDict:
        """Sum the contribution of each ingredient to a recipe's overall
        Flavor, Power, or Pokémon Type.

        Args:
            attr_name: Name of attribute: `flavor`, `power`, or `pokemon_type`

        Returns:
            A dictionary mapping each attribute to its sum
        """
        if self.recipe is None:
            raise ValueError("No recipe")

        if attr_name == "type":
            attr_name = "pokemon_type"
        elif attr_name not in ("flavor", "power", "pokemon_type"):
            raise ValueError(f"Unrecognized attribute: {attr_name}.")

        raw_attr_sum = defaultdict(int)
        for ingredient in self.recipe.ingredients:
            for attr, value in getattr(ingredient, attr_name).items():
                pieces = getattr(ingredient, "pieces", 1)
                raw_attr_sum[attr] += value * pieces
        attr_sum = self.sort_attr_sum(raw_attr_sum)
        attr_sum = {attr: value for attr, value in attr_sum.items() if value != 0}

        if attr_name == "flavor":
            # Force min two flavors in result
            if len(attr_sum) == 1:
                for flavor in Flavor._member_map_.values():
                    if flavor not in attr_sum:
                        attr_sum[flavor] = 0
                        break

        if attr_name == "pokemon_type":
            # Force min three types in result
            while len(attr_sum) < 3:
                for type_ in Type._member_map_.values():
                    if type_ not in attr_sum:
                        attr_sum[type_] = 0
                        break

        return attr_sum

    def compute_effects(self) -> list[EffectTuple]:
        """Compute the effects of a recipe.

        Returns:
            List of tuples containing a Power, a Pokémon Type, and a Level.
        """
        flavor_sum = self.get_attr_sum("flavor")
        power_sum = self.get_attr_sum("power")
        type_sum = self.get_attr_sum("pokemon_type")

        # Apply Flavor combo bonus to Power sum
        dominant_flavor1, dominant_flavor2, *_ = flavor_sum.keys()
        boosted_power = FLAVOR_COMBO_BONUS[(dominant_flavor1, dominant_flavor2)]
        if boosted_power in power_sum:
            power_sum[boosted_power] += 100
        else:
            power_sum[boosted_power] = 100
        power_sum = self.sort_attr_sum(power_sum)

        # Use dominant Type list to compute final Type order and effect Levels
        dominant_types = [*type_sum.items()][:3]
        for type_, value in dominant_types:
            self.dominant_types.append(type_)
            self.dominant_type_values.append(value)

        sorted_types = self.sort_types()
        levels = self.compute_levels()

        filtered_powers = [
            power
            for power, value in power_sum.items()
            if (power != Power.SPARKLING) or (value >= 2000)
        ][:3]

        return [*zip(filtered_powers, sorted_types, levels)]

    def sort_types(self) -> tuple[Type, Type, Type]:
        """Sort the Type of the recipe's effects.

        Returns:
            Final three Types associated with each recipe effect
        """
        if not self.dominant_types:
            raise ValueError("Dominant Types have not been computed")

        assert len(self.dominant_types) == 3
        types = self.dominant_types
        values = self.dominant_type_values
        difference = values[0] - values[1]

        if values[0] > 480:
            return (types[0], types[0], types[0])
        elif values[0] > 280:
            return (types[0], types[0], types[2])
        else:
            split = False
            if values[0] > 105 and difference > 105:
                return (types[0], types[0], types[2])
            elif 100 <= values[0] <= 105:
                split = difference >= 80 and values[1] <= 21
            elif 90 <= values[0] < 100:
                split = difference >= 78 and values[1] <= 16
            elif 80 <= values[0] < 90:
                split = difference >= 74 and values[1] <= 9
            elif 74 <= values[0] < 80:
                split = difference >= 72 and values[1] <= 5
            if split:
                return (types[0], types[2], types[0])
            return (types[0], types[2], types[1])

    def compute_levels(self) -> tuple[int, int, int]:
        """Calculate the Levels of each effect.

        Returns:
            Three Levels associated with each recipe effect
        """
        if not self.dominant_type_values:
            raise ValueError("Dominant Types have not been computed")

        first_value, second_value, third_value = self.dominant_type_values
        if first_value < 180:
            return (1, 1, 1)
        elif first_value <= 280:
            if second_value >= 180 and third_value >= 180:
                return (2, 2, 1)
            else:
                return (2, 1, 1)
        elif first_value < 380:
            if third_value >= 180:
                return (2, 2, 2)
            else:
                return (2, 2, 1)
        elif first_value < 460:
            if second_value >= 380 and third_value >= 380:
                return (3, 3, 3)
            else:
                return (3, 3, 2)
        else:
            return (3, 3, 3)


calculate_effects = EffectCalculator()
