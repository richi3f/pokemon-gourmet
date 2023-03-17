__all__ = ["random_rollout_policy"]

import random
from typing import Callable

from pokemon_picnic.suggester.mcts.action import Action, FinishSandwich
from pokemon_picnic.suggester.mcts.state import Sandwich, State

RolloutPolicy = Callable[..., Action]


def random_rollout_policy(state: State) -> Action:
    """A rollout policy that gives ingredients a uniform probability of being
    picked."""
    possible_actions = state.get_possible_actions()
    return random.choice(possible_actions)


def short_recipe_rollout_policy(state: State, prob: float = 0.5) -> Action:
    """A rollout policy that favors short recipes (i.e., the action to finish
    the sandwich has higher probability of being picked).

    Args:
        state: Current state
        prob: Probability. Chance to select the finish a sandwich action.

    Raises:
        ValueError: When `prob` is not between 0 and 1.
    """
    possible_actions = state.get_possible_actions()
    try:
        finish_idx = possible_actions.index(FinishSandwich())
    except ValueError:
        return random.choice(possible_actions)
    if not 0.0 <= prob <= 1.0:
        raise ValueError("Probability must be between 0 and 1.")
    weights = [1.0] * len(possible_actions)
    weights[finish_idx] = prob / (1 - prob) * (len(possible_actions) - 1)
    return random.choices(possible_actions, weights, k=1)[0]


# TODO: policy take into account ingredient properties
# TODO: policy take into account ingredient price/number
