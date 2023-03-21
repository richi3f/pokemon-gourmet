__all__ = ["Sandwich", "State"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from itertools import filterfalse, product
from operator import attrgetter

from pokemon_gourmet.enums import Power
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient import Ingredient
from pokemon_gourmet.sandwich.ingredient_data import (
    CONDIMENTS,
    FILLINGS,
    INGREDIENTS,
)
from pokemon_gourmet.sandwich.recipe import Recipe
from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectBaseRecipe,
    SelectCondiment,
    SelectFilling,
    SelectIngredient,
)

IS_HERBA_MYSTICA = attrgetter("is_herba_mystica")


class State(metaclass=ABCMeta):
    """A transitory description of an environment (e.g., a sandwich recipe)"""

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
    """A recipe in the making"""

    def __init__(self, targets: EffectList) -> None:
        super().__init__([], [])
        if len(targets) != 3:
            raise ValueError("Target effects should be exactly three.")
        self.targets = targets
        self._is_finished = False

    def __bool__(self) -> bool:
        return self.get_reward() >= 1

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
            possible_actions.append(FinishSandwich())
            if len(self.condiments) < 4:
                # Force second condiment to be Herba Mystica if Sparkling Power
                if Power.SPARKLING in self.targets.powers and len(self.condiments) == 1:
                    valid_condiments = filter(IS_HERBA_MYSTICA, CONDIMENTS)
                # Otherwise, exclude Herba Mystica from recipe
                else:
                    valid_condiments = filterfalse(IS_HERBA_MYSTICA, CONDIMENTS)
                for ingredient in valid_condiments:
                    possible_actions.append(SelectCondiment(ingredient.name))

            if len(self.fillings) < 6:
                for ingredient in FILLINGS:
                    possible_actions.append(SelectFilling(ingredient.name))
        return possible_actions

    def get_reward(self) -> float:
        """Calculate the score of this recipe by comparing its calculated
        effects with the desired effects. Although only effect Power and Type
        are matched, effect levels are used as bonus multipliers."""
        if self.is_legal:
            effects = self.effects
            levels = effects.remove_levels()  # do not compare levels
            base_reward = len(self.targets & effects)
            # double reward if levels are maximum
            bonus_reward = 100 * sum(levels) if base_reward == 3 else 3
            return bonus_reward * base_reward / 9
        return 0

    def move(self, action: Action) -> "State":
        """Generate a new state (recipe) by applying an action to the current
        one. Actions can either mark the recipe as finished or add ingredients
        to the list of ingredients.

        Returns:
            A copy of the recipe that is either marked as finished or has
            additional ingredients
        """
        next_state = deepcopy(self)
        if isinstance(action, FinishSandwich):
            next_state.is_finished = True
        elif isinstance(action, SelectIngredient):
            ingredient = INGREDIENTS[action.ingredient_name]
            next_state.add_ingredient(ingredient)
        elif isinstance(action, SelectBaseRecipe):
            for ingredient_name in action:
                next_state.add_ingredient(INGREDIENTS[ingredient_name])
        else:
            raise TypeError("Unknown action type")
        return next_state
