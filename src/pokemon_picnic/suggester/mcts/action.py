__all__ = ["Action", "FinishSandwich", "SelectCondiment", "SelectFilling"]

from collections.abc import Hashable
from dataclasses import dataclass


class Action(Hashable):
    ...


class FinishSandwich(Action):
    def __eq__(self, other: "FinishSandwich") -> bool:
        return self.__class__ == other.__class__

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass(unsafe_hash=True)
class SelectIngredient(Action):
    ingredient_name: str

    def __eq__(self, other: "SelectIngredient") -> bool:
        return (
            self.__class__ == other.__class__
            and self.ingredient_name == other.ingredient_name
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.ingredient_name})"


@dataclass(unsafe_hash=True)
class SelectCondiment(SelectIngredient):
    ...


@dataclass(unsafe_hash=True)
class SelectFilling(SelectIngredient):
    ...
