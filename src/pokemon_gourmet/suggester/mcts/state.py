__all__ = ["Sandwich", "State"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy

from pokemon_gourmet.enums import Power
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient_data import (
    CONDIMENTS,
    FILLINGS,
    INGREDIENTS,
)
from pokemon_gourmet.sandwich.recipe import Recipe
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


class Sandwich(Recipe, State):
    def __init__(self, targets: EffectList) -> None:
        super().__init__([], [])
        if len(targets) != 3:
            raise ValueError("Target effects should be exactly three.")
        self.targets = targets
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
                    Power.TITLE not in self.targets.powers
                    or (
                        Power.SPARKLING not in self.targets.powers
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
            effects = self.effects
            levels = effects.remove_levels()  # do not compare levels
            base_reward = len(self.targets & effects)
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
            next_state.add_ingredient(ingredient)
        return next_state
