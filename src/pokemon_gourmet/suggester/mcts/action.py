__all__ = [
    "Action",
    "FinishSandwich",
    "SelectBaseRecipe",
    "SelectCondiment",
    "SelectFilling",
]

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pokemon_gourmet.sandwich.ingredient_data import INGREDIENTS

if TYPE_CHECKING:
    from pokemon_gourmet.suggester.mcts.state import Sandwich, State


class Action(metaclass=ABCMeta):
    """A trigger for a state transition"""

    @abstractmethod
    def __call__(self, state: "State") -> None:
        raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        ...


class FinishSandwich(Action):
    """Finalize a recipe"""

    def __call__(self, state: "Sandwich") -> None:
        state.is_finished = True

    def __eq__(self, other: "FinishSandwich") -> bool:
        return self.__class__ == other.__class__

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass(unsafe_hash=True)
class SelectBaseRecipe(Action, Iterable):
    """Select a condiment and a filling to start a recipe with"""

    condiment_name: str
    filling_name: str

    def __call__(self, state: "Sandwich") -> None:
        for ingredient_name in self:
            state.add_ingredient(INGREDIENTS[ingredient_name])

    def __eq__(self, other: "SelectBaseRecipe") -> bool:
        return (
            self.__class__ == other.__class__
            and self.condiment_name == other.condiment_name
            and self.filling_name == other.filling_name
        )

    def __iter__(self) -> Iterator[str]:
        return iter((self.condiment_name, self.filling_name))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.condiment_name}, {self.filling_name})"


@dataclass(unsafe_hash=True)
class SelectIngredient(Action):
    """Select an ingredient to add to a recipe's list of ingredients"""

    ingredient_name: str

    def __call__(self, state: "Sandwich") -> None:
        state.add_ingredient(INGREDIENTS[self.ingredient_name])

    def __eq__(self, other: "SelectIngredient") -> bool:
        return (
            self.__class__ == other.__class__
            and self.ingredient_name == other.ingredient_name
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.ingredient_name})"


@dataclass(unsafe_hash=True)
class SelectCondiment(SelectIngredient):
    """Select a condiment to add to a recipe's list of ingredients"""

    ...


@dataclass(unsafe_hash=True)
class SelectFilling(SelectIngredient):
    """Select a filling to add to a recipe's list of ingredients"""

    ...
