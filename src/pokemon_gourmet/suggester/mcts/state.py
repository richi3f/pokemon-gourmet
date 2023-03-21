__all__ = ["Sandwich", "State"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from itertools import product
from math import log2
from typing import Any, Iterator, TypeVar, Union

from pokemon_gourmet.enums import Power
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient import Ingredient
from pokemon_gourmet.sandwich.ingredient_data import CONDIMENTS, FILLINGS
from pokemon_gourmet.sandwich.recipe import Recipe, RecipeTuple
from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectBaseRecipe,
    SelectCondiment,
    SelectFilling,
)

REWARD_GROWTH_FACTOR = log2(300) / 6

S = TypeVar("S", bound="State")


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
    def get_reward(self) -> float:
        ...

    @abstractmethod
    def move(self: S, action: Action) -> S:
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

    def __init__(self, targets: EffectList) -> None:
        super().__init__([], [])
        if len(targets) != 3:
            raise ValueError("Target effects should be exactly three.")
        self.targets = targets
        self._is_finished = False

    def __bool__(self) -> bool:
        return self.get_reward() >= 1

    def __lt__(self, other: "Sandwich") -> bool:
        rhs = (self.get_reward(), -len(self.condiments), -len(self.fillings))
        lhs = (other.get_reward(), -len(other.condiments), -len(other.fillings))
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
            len(self.fillings) == 6 and len(self.condiments) == 4
        )

    def exists(self, ingredient: Ingredient) -> bool:
        """Check whether adding an ingredient would result in an existing
        recipe."""
        ingredient_names = [ingredient.name]
        ingredient_names += [ingredient.name for ingredient in self.ingredients]
        tup = tuple(sorted(ingredient_names))
        return tup in recipe_manager

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
        possible_actions = []
        if len(self) == 0:

            def validate_condiment(condiment: Ingredient) -> bool:
                return not (
                    condiment.is_herba_mystica
                    ^ (
                        Power.TITLE in self.targets.powers
                        or Power.SPARKLING in self.targets.powers
                    )
                )

            # Force base recipe to include Herba Mystica if Title/Sparkling Power
            valid_condiments = filter(validate_condiment, CONDIMENTS)
            for condiment, filling in product(valid_condiments, FILLINGS):
                possible_actions.append(SelectBaseRecipe(condiment.name, filling.name))
        else:
            # Force second condiment to be Herba Mystica if Sparkling Power
            if Power.SPARKLING in self.targets.powers and len(self.condiments) == 1:
                for ingredient in CONDIMENTS:
                    if ingredient.is_herba_mystica:
                        possible_actions.append(SelectCondiment(ingredient.name))
            else:
                possible_actions.append(FinishSandwich())
                if len(self.condiments) < 4:
                    # Exclude Herba Mystica from recipe
                    # Skip condiment if it would render an existing recipe
                    for ingredient in CONDIMENTS:
                        if ingredient.is_herba_mystica or self.exists(ingredient):
                            continue
                        possible_actions.append(SelectCondiment(ingredient.name))

                if len(self.fillings) < 6:
                    for ingredient in FILLINGS:
                        # Skip ingredient if it would render an existing recipe
                        if self.exists(ingredient):
                            continue
                        possible_actions.append(SelectFilling(ingredient.name))
        return possible_actions

    def get_reward(self) -> float:
        """Calculate the score of this recipe by comparing its calculated
        effects with the desired effects.

        Score is zero is there is no match between recipe's computed effects
        and desired effects, and it is one if there's an exact match. If
        there's an exact match, the score is one. It is doubled at a rate so
        that if all target effects are at Level 3, the score becomes 300.

        Returns:
            A score in the range of [0, 300]
        """
        if self.is_legal:
            effects = self.effects
            levels = effects.remove_levels()  # Do not compare levels
            base_reward = len(self.targets & effects) / 3
            if base_reward == 1.0:
                # Grow exponentially according to Level sum
                return 2 ** (REWARD_GROWTH_FACTOR * (sum(levels) - 3))
            return base_reward
        return 0

    def move(self, action: Action) -> "State":
        """Copy current recipe and generate a new one by doing an action on the
        current recipe (state). Actions can either mark the recipe as finished
        or add ingredients to the list of ingredients.

        Returns:
            The new recipe
        """
        next_state = deepcopy(self)
        action(next_state)
        return next_state


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RecipeManager(metaclass=Singleton):
    """Manage generated recipes by keeping a list of unique entries"""

    def __init__(self) -> None:
        self._states: set[RecipeTuple] = set()

    def __contains__(self, item: Union[Sandwich, RecipeTuple]) -> bool:
        if isinstance(item, Sandwich):
            item = item.astuple()
        if isinstance(item, tuple):
            return item in self._states
        raise TypeError()

    def __iter__(self) -> Iterator[RecipeTuple]:
        return iter(self._states)

    def __len__(self) -> int:
        return len(self._states)

    def __repr__(self) -> str:
        s = "s" if len(self) != 1 else ""
        return f"{self.__class__.__name__}({len(self)} state{s})"

    def add(self, item: State) -> None:
        """Add a recipe (as a tuple) to the recipe manager."""
        if isinstance(item, Sandwich):
            tup = item.astuple()
            return self._states.add(tup)
        raise TypeError(f"Received {type(item)}, should be `State`")

    def clear(self) -> None:
        """Remove all items from the recipe manager."""
        self._states.clear()


recipe_manager = RecipeManager()
