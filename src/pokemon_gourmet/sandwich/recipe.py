__all__ = ["Recipe"]

from collections import defaultdict
from collections.abc import Collection, Hashable, Iterator
from operator import itemgetter
from typing import Any, cast

from pokemon_gourmet.enums import Flavor, Power, Type
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient import Condiment, Filling, Ingredient
from pokemon_gourmet.sandwich.ingredient_data import INGREDIENTS

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


def sort_attr_sum(attr_sum: dict[Any, int]) -> dict[Any, int]:
    return dict(
        sorted(attr_sum.items(), key=lambda kvp: (kvp[1], -kvp[0].value), reverse=True)
    )


def calculate_levels(dominant_types: list[tuple[Type, int]]) -> tuple[int, int, int]:
    first_value, second_value, third_value = map(itemgetter(1), dominant_types)
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


def sort_types(dominant_types: list[tuple[Type, int]]) -> tuple[Type, Type, Type]:
    assert len(dominant_types) == 3
    types, values = zip(*dominant_types)
    types, values = cast(tuple[Type, ...], types), cast(tuple[int, ...], values)
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
            ingredients[isinstance(ingredient, Filling)].append(ingredient)
        recipe = cls(*ingredients)
        if recipe.is_legal:
            return recipe
        raise ValueError("Recipe is not legal.")

    @property
    def effects(self) -> EffectList:
        if self._effects is None:
            _, power_sum, type_sum = self._get_attr_sums().values()
            dominant_types = [*type_sum.items()][:3]
            types = sort_types(dominant_types)
            levels = calculate_levels(dominant_types)
            powers = [
                power
                for power, value in power_sum.items()
                if (power != Power.SPARKLING) or (value >= 2000)
            ][:3]
            self._effects = [*zip(powers, types, levels)]
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

    def _get_attr_sum(self, attr_name: str) -> dict[Any, int]:
        if attr_name == "type":
            attr_name = "pokemon_type"
        elif attr_name not in ("flavor", "power", "pokemon_type"):
            raise ValueError(f"Unrecognized attribute: {attr_name}.")

        raw_attr_sum = defaultdict(int)
        for ingredient in self.ingredients:
            for attr, value in getattr(ingredient, attr_name).items():
                pieces = getattr(ingredient, "pieces", 1)
                raw_attr_sum[attr] += value * pieces
        attr_sum = sort_attr_sum(raw_attr_sum)
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

    def _get_attr_sums(self) -> dict[str, dict[Any, int]]:
        attrs = {}
        for attr_name in ("flavor", "power", "pokemon_type"):
            attrs[attr_name] = self._get_attr_sum(attr_name)

        # Apply flavor combo bonus to power
        flavor = cast(dict[Flavor, int], attrs["flavor"])
        dominant_flavor1, dominant_flavor2, *_ = flavor.keys()
        boosted_power = FLAVOR_COMBO_BONUS[(dominant_flavor1, dominant_flavor2)]
        if boosted_power in attrs["power"]:
            attrs["power"][boosted_power] += 100
        else:
            attrs["power"][boosted_power] = 100
        attrs["power"] = sort_attr_sum(attrs["power"])

        return attrs

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """Add ingredient to recipe and reset its effects."""
        self._effects = None  # Reset effects
        if ingredient.is_condiment:
            self.condiments.append(cast(Condiment, ingredient))
        else:
            self.fillings.append(cast(Filling, ingredient))

    def __contains__(self, ingredient: Ingredient) -> bool:
        if ingredient.is_condiment:
            return ingredient in self.condiments
        return ingredient in self.fillings

    def __hash__(self) -> int:
        return hash(tuple([ingredient.name for ingredient in sorted(self.ingredients)]))

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
