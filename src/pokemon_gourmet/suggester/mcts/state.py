__all__ = ["Sandwich", "State", "Target"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from dataclasses import astuple, dataclass
from typing import Iterator, Union, Optional, Sequence, cast

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.ingredient import Condiment, Filling
from pokemon_gourmet.sandwich.ingredient_data import (
    CONDIMENTS,
    FILLINGS,
    INGREDIENTS,
)
from pokemon_gourmet.sandwich.recipe import Effect, Recipe
from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectCondiment,
    SelectFilling,
    SelectIngredient,
)


class State(metaclass=ABCMeta):
    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        ...

    @abstractmethod
    def get_possible_actions(self) -> list[Action]:
        ...

    @abstractmethod
    def get_reward(self) -> float:
        ...

    @abstractmethod
    def move(self, action: Action) -> "State":
        ...


@dataclass
class Target:
    power: Power
    pokemon_type: Optional[Type]

    @classmethod
    def from_effect(cls, effect: Effect) -> "Target":
        type_ = None if effect.power == Power.EGG else effect.pokemon_type
        return cls(effect.power, type_)

    def __iter__(self) -> Iterator[Union[Power, Type, None]]:
        return iter(astuple(self))

    def __hash__(self) -> int:
        type_ = None if self.pokemon_type is None else self.pokemon_type.value
        return hash((self.power.value, type_))

    def __repr__(self) -> str:
        repr = f"{self.power.name} Power"
        if self.pokemon_type is not None:
            repr += f": {self.pokemon_type.name}"
        return repr


class Sandwich(Recipe, State):
    def __init__(self, targets: Sequence[Target]) -> None:
        super().__init__([], [])
        if len(targets) != 3:
            raise ValueError("Target effects should be exactly three.")
        self.targets = set(targets)
        self.target_powers = set(target.power for target in self.targets)
        self._is_finished = False

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    @is_finished.setter
    def is_finished(self, value: bool) -> None:
        self._is_finished = value

    @property
    def is_terminal(self) -> bool:
        return self.is_finished or (
            len(self.fillings) == 6 and len(self.condiments) == 4
        )

    def get_possible_actions(self) -> list[Action]:
        possible_actions = []
        if self.is_legal:
            possible_actions.append(FinishSandwich())
        if len(self.condiments) < 4:
            for ingredient in CONDIMENTS:
                # Title power requires Herba Mystica
                # Sparkling power requires two Herba Mystica
                if ingredient.is_herba_mystica and (
                    Power.TITLE not in self.target_powers
                    or (
                        Power.SPARKLING not in self.target_powers
                        and self.has_herba_mystica
                    )
                ):
                    continue
                possible_actions.append(SelectCondiment(ingredient.name))
        if len(self.fillings) < 6:
            for ingredient in FILLINGS:
                possible_actions.append(SelectFilling(ingredient.name))
        return possible_actions

    def get_reward(self) -> float:
        if self.is_legal:
            effects, levels = [], []
            for effect in self.effects:
                effects.append(Target.from_effect(effect))
                levels.append(effect.level)
            base_reward = len(self.targets.intersection(effects))
            # double reward if levels are maximum
            bonus_reward = (sum(levels) + 3) / 6 if base_reward == 3 else 1.0
            return bonus_reward * base_reward / 3
        return 0

    def move(self, action: Action) -> "State":
        next_state = deepcopy(self)
        if isinstance(action, FinishSandwich):
            next_state.is_finished = True
        elif isinstance(action, SelectIngredient):
            ingredient = INGREDIENTS[action.ingredient_name]
            if ingredient.is_condiment:
                next_state.condiments.append(cast(Condiment, ingredient))
            else:
                next_state.fillings.append(cast(Filling, ingredient))
        return next_state
