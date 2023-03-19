__all__ = ["Condiment", "Filling", "Ingredient"]

from dataclasses import dataclass, field
from typing import Union

from pokemon_gourmet.enums import Flavor, Power, Type


@dataclass
class _IngredientBase:
    name: str

    @property
    def is_condiment(self) -> bool:
        return not self.is_filling

    @property
    def is_filling(self) -> bool:
        raise NotImplementedError

    @property
    def is_herba_mystica(self) -> bool:
        return False

    def __lt__(self, other: "_IngredientBase") -> bool:
        return self.name < other.name

    def __eq__(self, other: "_IngredientBase") -> bool:
        return self.__class__ == other.__class__ and self.name == other.name


@dataclass
class _IngredientProperties:
    flavor: dict[Flavor, int] = field(default_factory=dict, repr=False)
    power: dict[Power, int] = field(default_factory=dict, repr=False)
    pokemon_type: dict[Type, int] = field(default_factory=dict, repr=False)


@dataclass
class _FillingBase(_IngredientBase):
    pieces: int

    @property
    def is_filling(self) -> bool:
        return True


@dataclass
class Condiment(_IngredientProperties, _IngredientBase):
    @property
    def is_filling(self) -> bool:
        return False

    @property
    def is_herba_mystica(self) -> bool:
        return "Herba Mystica" in self.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Filling(_IngredientProperties, _FillingBase):
    def __hash__(self) -> int:
        return hash(self.name)


Ingredient = Union[Condiment, Filling]
