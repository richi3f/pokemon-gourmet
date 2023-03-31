__all__ = ["Sandwich", "State", "recipe_manager"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from itertools import product
from math import log2
from typing import Generic, Hashable, Iterator, TypeVar, Union, cast

import numpy as np

from pokemon_gourmet.enums import Power
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient_data import ingredient_data
from pokemon_gourmet.sandwich.recipe import (
    MAX_CONDIMENTS,
    MAX_FILLINGS,
    Ingredient,
    Recipe,
    RecipeTuple,
)
from pokemon_gourmet.singleton import Singleton
from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectBaseRecipe,
    SelectCondiment,
    SelectFilling,
)

REWARD_GROWTH_FACTOR = log2(300) / 2

StateT = TypeVar("StateT", bound="State")
State_co = TypeVar("State_co", bound="State", covariant=True)
T_co = TypeVar("T_co", bound=Hashable, covariant=True)


class State(metaclass=ABCMeta):
    """A description of a transitional situation (e.g., making a sandwich recipe)"""

    @abstractmethod
    def __hash__(self) -> int:
        ...

    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        ...

    @abstractmethod
    def get_possible_actions(self) -> list[Action]:
        ...

    @abstractmethod
    def move(self: StateT, action: Action) -> StateT:
        ...

    @property
    @abstractmethod
    def reward(self) -> float:
        ...


class Sandwich(Recipe, State):
    """A recipe in the making.

    This recipe starts with an empty list of ingredients and progressively
    gets additions to this list through actions selected by the MCTS algorithm.

    Note unlike the parent `Recipe` class, instances of this class evaluate to
    True if their computed effects match their desired effects. Additionally,
    these recipes can be sorted by comparing the matching score and the number
    of condiments and fillings.
    """

    def __init__(
        self,
        targets: EffectList,
        min_fillings: int = 1,
        max_fillings: int = MAX_FILLINGS,
        num_players: int = 1,
    ) -> None:
        super().__init__(num_players=num_players)
        if not 0 < len(targets) <= 3:
            raise ValueError("Target effects should be between one and three.")
        self.targets = targets
        if max_fillings < min_fillings:
            raise ValueError(
                "The maximum number of fillings cannot be less than the mininum"
                "number of fillings"
            )
        self.min_fillings = max(1, min_fillings) * num_players
        self.max_fillings = min(MAX_FILLINGS, max_fillings) * num_players
        self.max_condiments = MAX_CONDIMENTS * num_players
        self._is_finished = False
        self._reward = None

    def __bool__(self) -> bool:
        return bool(self.reward >= 1)

    def __lt__(self, other: "Sandwich") -> bool:
        rhs = (
            self.reward,
            -self.num_fillings,
            -self.total_pieces,
            -self.num_condiments,
        )
        lhs = (
            other.reward,
            -other.num_fillings,
            -self.total_pieces,
            -other.num_condiments,
        )
        return rhs < lhs

    @property
    def is_finished(self) -> bool:
        """Whether this recipe has been marked as finished and will not receive
        any additional ingredients"""
        return self._is_finished

    @is_finished.setter
    def is_finished(self, value: bool) -> None:
        self._is_finished = value

    @property
    def is_terminal(self) -> bool:
        """Whether this recipe is finished or it has no more room for any
        additional ingredient"""
        return self.is_finished or (
            self.num_fillings == self.max_fillings
            and self.num_condiments == self.max_condiments
        )

    @property
    def reward(self) -> float:
        """The recipe's score:

        - 0.000 - if it does not match any target effect
        - 0.333 - if it matches one target effect
        - 0.667 - if it matches two target effects
        - 1.000 - if it matches all three target effects at Lv. 1
        - 17.32 - if it matches all three target effects at Lv. 2
        - 300.0 - if it matches all three target effects at Lv. 3
        """
        if self._reward is None:
            self._reward = self.get_reward()
        return self._reward

    def add_ingredient(self, ingredient: Ingredient) -> None:
        self._reward = None  # Reset reward
        return super().add_ingredient(ingredient)

    def exists_with(self, ingredient: Ingredient) -> bool:
        """Check whether adding an ingredient would result in an existing
        recipe."""
        i = self._get_ingredient_index(ingredient)
        list_ = self._ingredient_list.tolist()
        list_[i] += 1
        return tuple(list_) in recipe_manager

    def get_possible_actions(self) -> list[Action]:
        """Return a list of possible actions.

        If the recipe is empty, return a list of `SelectBaseRecipe` actions.
        A base recipe consists of one condiment and one filling. If the desired
        effects include Title or Sparkling Power, the condiment will be a Herba
        Mystica.

        If the recipe already has ingredients, return a list with one
        `FinishSandwich` action and one `SelectIngredient` action for each
        valid condiment and filling. Valid condiments are all condiments,
        except Herba Mystica (unless the desired effects include Sparkling
        Power and the sandwich only has one condiment).

        These rules guarantee that recipes have only the strictly necessary
        number of Herba Mystica: one if Title Power desired or two if Sparkling
        Power desired.
        """
        can_stop = False
        possible_actions = []
        if len(self) == 0:
            # Force base recipe to include Herba Mystica if Title/Sparkling Power
            # Sparkling is always paired with Title, so only check Title
            title = Power.TITLE in self.targets
            valid_condiments = np.flatnonzero(
                ingredient_data.is_condiment
                & ~(ingredient_data.is_herba_mystica ^ title)
            )
            valid_fillings = np.flatnonzero(ingredient_data.is_filling)
            for condiment, filling in product(valid_condiments, valid_fillings):
                possible_actions.append(SelectBaseRecipe(condiment, filling))
        else:
            # Force second condiment to be Herba Mystica if Sparkling Power
            if Power.SPARKLING in self.targets and self.num_condiments == 1:
                for ingredient in np.flatnonzero(ingredient_data.is_herba_mystica):
                    possible_actions.append(SelectCondiment(ingredient))
            else:
                # Add fillings if there is room
                if self.num_fillings < self.max_fillings:
                    # Skip fillings that have reached max number of pieces
                    ingredient_counts = self._ingredient_list * ingredient_data.pieces
                    valid_fillings = np.flatnonzero(
                        ingredient_data.is_filling
                        & (ingredient_counts <= self.single_ingredient_limit)
                    )
                    for ingredient in valid_fillings:
                        # Skip ingredients that generate redundant recipes
                        if self.exists_with(ingredient):
                            continue
                        possible_actions.append(SelectFilling(ingredient))

                # If min # of fillings have been added, make it possible to stop
                # or select condiments
                if self.num_fillings >= self.min_fillings:
                    can_stop = True

                    if self.num_condiments < self.max_condiments:
                        # Exclude Herba Mystica from recipe
                        valid_condiments = np.flatnonzero(
                            ingredient_data.is_condiment
                            & ~ingredient_data.is_herba_mystica
                        )
                        for ingredient in valid_condiments:
                            # Skip ingredients that generate redundant recipes
                            if self.exists_with(ingredient):
                                continue
                            possible_actions.append(SelectCondiment(ingredient))
        # Add stopping action if no other action possible
        if can_stop or len(possible_actions) == 0:
            possible_actions.append(FinishSandwich())
        return possible_actions

    def get_reward(self) -> float:
        """Calculate the score of this recipe by comparing its calculated
        effects with the desired Meal Powers.

        Score is zero is there is no match between recipe's computed effects
        and desired effects, and it is one if there's an exact match. If
        there's an exact match, the score is doubled at a rate so that if all
        target effects are at Level 3, the score becomes 300.

        Returns:
            A score in the range of [0, 300]
        """
        if self.is_legal:
            effects = self.effects
            levels = effects.remove_levels()  # Do not compare Levels
            intersection = cast(EffectList, self.targets & effects)
            base_reward = len(intersection) / len(self.targets)
            if base_reward == 1.0:
                if len(self.targets) < 3:
                    # Only use Levels of matching Meal Powers
                    levels = [
                        levels[self.targets.index(i)] for i in intersection.powers
                    ]
                level_sum = (sum(levels) / len(levels)) - 1
                # Grow exponentially according to Level sum
                return 2 ** (REWARD_GROWTH_FACTOR * level_sum)
            return base_reward
        return 0

    def move(self, action: Action) -> "Sandwich":
        """Copy current recipe and generate a new one by doing an action on the
        current recipe (state). Actions can either mark the recipe as finished
        or add ingredients to the list of ingredients.

        Returns:
            The new recipe
        """
        next_state = deepcopy(self)
        action(next_state)
        return next_state


class StateManager(Generic[State_co, T_co]):
    def __init__(self) -> None:
        self._states: set[T_co] = set()

    def __contains__(self, item: Union[State_co, T_co]) -> bool:
        return item in self._states

    def __iter__(self) -> Iterator[T_co]:
        return iter(self._states)

    def __len__(self) -> int:
        return len(self._states)

    def __repr__(self) -> str:
        s = "s" if len(self) != 1 else ""
        return f"{self.__class__.__name__}({len(self)} state{s})"

    def add(self, item: Union[State_co, T_co]) -> None:
        """Add a recipe (as a tuple) to the recipe manager."""
        return self._states.add(cast(T_co, item))

    def clear(self) -> None:
        """Remove all items from the recipe manager."""
        self._states.clear()


class RecipeManager(StateManager[Sandwich, RecipeTuple], metaclass=Singleton):
    """Manage generated recipes by keeping a list of unique entries"""

    def __contains__(self, item: Union[Sandwich, RecipeTuple]) -> bool:
        if isinstance(item, Sandwich):
            item = item.astuple()
        if isinstance(item, tuple):
            return item in self._states
        raise TypeError()

    def add(self, item: Sandwich) -> None:
        """Add a recipe (as a tuple) to the recipe manager."""
        if isinstance(item, Sandwich):
            tup = item.astuple()
            return self._states.add(tup)
        raise TypeError(f"Received {type(item)}, should be `State`")


recipe_manager = RecipeManager()
