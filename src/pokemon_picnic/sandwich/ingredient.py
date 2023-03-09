__all__ = ["Condiment", "Filling"]

from dataclasses import dataclass, field
from typing import Union

from pokemon_picnic.core.enums import Flavor, Power, Type


@dataclass
class _IngredientBase:
    name: str


@dataclass
class _IngredientProperties:
    flavor: dict[Flavor, int] = field(default_factory=dict, repr=False)
    power: dict[Power, int] = field(default_factory=dict, repr=False)
    pokemon_type: dict[Type, int] = field(default_factory=dict, repr=False)


@dataclass
class _FillingBase(_IngredientBase):
    pieces: int


@dataclass
class Condiment(_IngredientProperties, _IngredientBase):
    pass


@dataclass
class Filling(_IngredientProperties, _FillingBase):
    pass


Ingredient = Union[Condiment, Filling]
