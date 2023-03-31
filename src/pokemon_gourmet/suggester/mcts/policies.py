__all__ = [
    "early_stopping_rollout_policy",
    "random_rollout_policy",
    "ROLLOUT_POLICIES",
    "weighted_allocation_rollout_policy",
]

import random
from collections import Counter
from typing import Callable

from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectBaseRecipe,
    SelectCondiment,
    SelectFilling,
)
from pokemon_gourmet.suggester.mcts.state import Sandwich, State

RolloutPolicy = Callable[..., Action]

ROLLOUT_POLICIES: dict[str, RolloutPolicy] = {}


def random_rollout_policy(state: State) -> Action:
    """A rollout policy that gives ingredients a uniform probability of being
    picked."""
    possible_actions = state.get_possible_actions()
    return random.choice(possible_actions)


ROLLOUT_POLICIES["random"] = random_rollout_policy


def early_stopping_rollout_policy(state: State, stop_prob: float = 0.5) -> Action:
    """A rollout policy that favors short recipes (i.e., the action to finish
    the sandwich has higher probability of being picked).

    Args:
        state:
            Current state
        stop_prob:
            Stopping probability. Chance to stop adding ingredients after the
            recipe has at least one condiment and filling.

    Raises:
        ValueError: When `stop_prob` is not between 0 and 1.
    """
    possible_actions = state.get_possible_actions()
    try:
        finish_idx = possible_actions.index(FinishSandwich())
    except ValueError:
        return random.choice(possible_actions)
    if not 0.0 < stop_prob <= 1.0:
        raise ValueError(
            "Probability must be greater than zero and equal or lower than 1."
        )
    weights = [1.0] * len(possible_actions)
    weights[finish_idx] = stop_prob / (1 - stop_prob) * (len(possible_actions) - 1)
    return random.choices(possible_actions, weights, k=1)[0]


ROLLOUT_POLICIES["early_stopping"] = early_stopping_rollout_policy


def weighted_allocation_rollout_policy(
    state: Sandwich, stop_prob: float = 0.1
) -> Action:
    """A rollout policy that weighs ingredients according to the free space in
    the sandwich. For instance, if a sandwich has five fillings and two
    condiments, the chance to finish a sandwich, add a filling, or add a
    condiment would be 10%, 60%, and 30%, respectively.

    Args:
        state:
            Current state
        stop_prob:
            Stopping probability. Chance to stop adding ingredients after the
            recipe has at least one condiment and filling.

    Raises:
        ValueError: When `stop_prob` is not between 0 and 1.
    """
    if not 0.0 < stop_prob < 1.0:
        raise ValueError("Probability must be between 0 and 1 (exclusive).")
    possible_actions = state.get_possible_actions()
    action_types = Counter(map(type, state.get_possible_actions()))
    if SelectBaseRecipe in action_types:
        return random.choice(possible_actions)
    free_slots = 10 * state.num_players - len(state)
    finish_weight = 100 * stop_prob * action_types[FinishSandwich]
    add_ingredient_weight = 100 - finish_weight
    add_filling_weight = (
        add_ingredient_weight * (state.max_fillings - state.num_fillings) / free_slots
    )
    add_condiment_weight = add_ingredient_weight - add_filling_weight
    weights = []
    for action in possible_actions:
        if isinstance(action, FinishSandwich):
            weights.append(finish_weight)
        elif isinstance(action, SelectCondiment):
            weights.append(add_condiment_weight / action_types[SelectCondiment])
        else:
            weights.append(add_ingredient_weight / action_types[SelectFilling])
    return random.choices(possible_actions, weights, k=1)[0]


ROLLOUT_POLICIES["weighted_allocation"] = weighted_allocation_rollout_policy

# TODO: policy take into account ingredient properties (flavors, powers, types)
