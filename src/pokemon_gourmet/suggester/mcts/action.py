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

from pokemon_gourmet.sandwich.ingredient_data import ingredient_data

if TYPE_CHECKING:
    from pokemon_gourmet.suggester.mcts.state import RecipeState, State


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

    def __call__(self, state: "RecipeState") -> None:
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

    condiment_idx: int
    filling_idx: int

    def __call__(self, state: "RecipeState") -> None:
        for ingredient_idx in self:
            state.add_ingredient(ingredient_idx)

    def __eq__(self, other: "SelectBaseRecipe") -> bool:
        return (
            self.__class__ == other.__class__
            and self.condiment_idx == other.condiment_idx
            and self.filling_idx == other.filling_idx
        )

    def __iter__(self) -> Iterator[int]:
        return iter((self.condiment_idx, self.filling_idx))

    def __repr__(self) -> str:
        condiment = ingredient_data[self.condiment_idx]
        filling = ingredient_data[self.filling_idx]
        return f"{self.__class__.__name__}({condiment}, {filling})"


@dataclass(unsafe_hash=True)
class SelectIngredient(Action):
    """Select an ingredient to add to a recipe's list of ingredients"""

    ingredient_idx: int

    def __call__(self, state: "RecipeState") -> None:
        state.add_ingredient(self.ingredient_idx)

    def __eq__(self, other: "SelectIngredient") -> bool:
        return (
            self.__class__ == other.__class__
            and self.ingredient_idx == other.ingredient_idx
        )

    def __repr__(self) -> str:
        ingredient = ingredient_data[self.ingredient_idx]
        return f"{self.__class__.__name__}({ingredient})"


@dataclass(unsafe_hash=True)
class SelectCondiment(SelectIngredient):
    """Select a condiment to add to a recipe's list of ingredients"""

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass(unsafe_hash=True)
class SelectFilling(SelectIngredient):
    """Select a filling to add to a recipe's list of ingredients"""

    def __repr__(self) -> str:
        return super().__repr__()
