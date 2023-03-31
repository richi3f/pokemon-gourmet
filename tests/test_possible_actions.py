import numpy as np
import pytest

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich import EffectList, ingredient_data
from pokemon_gourmet.suggester import mcts
from pokemon_gourmet.suggester.generator import parse_targets

NUM_CONDIMENTS = np.add.reduce(ingredient_data.is_condiment)
NUM_HERBA_MYSTICA = np.add.reduce(ingredient_data.is_herba_mystica)
NUM_FILLINGS = np.add.reduce(ingredient_data.is_filling)


def test_pedestrian_recipe():
    # No Sparkling/Title Power prevents Herba Mystica from being added to recipe
    desired_effects = [
        ("item_drop", "ice"),
        ("teensy", "bug"),
        ("raid", "fighting"),
    ]
    targets = parse_targets(desired_effects)
    initial_state = mcts.Sandwich(targets)

    first_actions = initial_state.get_possible_actions()
    assert len(first_actions) == (NUM_CONDIMENTS - NUM_HERBA_MYSTICA) * NUM_FILLINGS

    state = initial_state.move(first_actions[0])
    possible_actions = state.get_possible_actions()

    for _ in range(state.max_fillings - state.num_fillings):
        assert (
            len(possible_actions)
            == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + NUM_FILLINGS + 1
        )
        state.add_ingredient("Tofu")
        possible_actions = state.get_possible_actions()

    for _ in range(state.max_condiments - state.num_condiments):
        assert len(possible_actions) == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + 1
        state.add_ingredient("Ketchup")
        possible_actions = state.get_possible_actions()

    assert len(possible_actions) == 1


def test_title_power_recipe():
    # Title Power forces first action to include Herba Mystica
    desired_effects = [
        ("humungo", "dark"),
        ("title", "dark"),
        ("Encounter", "grass"),
    ]
    targets = parse_targets(desired_effects)
    initial_state = mcts.Sandwich(targets)
    first_actions = initial_state.get_possible_actions()

    assert len(first_actions) == NUM_HERBA_MYSTICA * NUM_FILLINGS

    state = initial_state.move(first_actions[0])
    possible_actions = state.get_possible_actions()

    for _ in range(state.max_fillings - state.num_fillings):
        assert (
            len(possible_actions)
            == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + NUM_FILLINGS + 1
        )
        state.add_ingredient("Chorizo")
        possible_actions = state.get_possible_actions()

    for _ in range(state.max_condiments - state.num_condiments):
        assert len(possible_actions) == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + 1
        state.add_ingredient("Wasabi")
        possible_actions = state.get_possible_actions()

    assert len(possible_actions) == 1


def test_sparkling_power_recipe():
    # Sparkling Power forces first two actions to include Herba Mystica
    desired_effects = [
        ("sparkling", "water"),
        ("title", "water"),
        ("catching", "water"),
    ]
    targets = parse_targets(desired_effects)
    initial_state = mcts.Sandwich(targets, max_fillings=4)
    first_actions = initial_state.get_possible_actions()

    assert len(first_actions) == NUM_HERBA_MYSTICA * NUM_FILLINGS

    state = initial_state.move(first_actions[0])
    second_actions = state.get_possible_actions()

    assert len(second_actions) == NUM_HERBA_MYSTICA

    state = state.move(second_actions[0])
    possible_actions = state.get_possible_actions()

    for _ in range(state.max_condiments - state.num_condiments):
        assert (
            len(possible_actions)
            == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + NUM_FILLINGS + 1
        )
        state.add_ingredient("Jam")
        possible_actions = state.get_possible_actions()

    for _ in range(state.max_fillings - state.num_fillings):
        assert len(possible_actions) == NUM_FILLINGS + 1
        state.add_ingredient("Basil")
        possible_actions = state.get_possible_actions()

    assert len(possible_actions) == 1

@pytest.mark.parametrize("min_fillings", range(2, 7))
def test_min_fillings_recipe(min_fillings: int):
    desired_effects = EffectList(
        [(Power.EXP_POINT, Type.DRAGON), (Power.TITLE, Type.STEEL)]
    )
    initial_state = mcts.Sandwich(desired_effects, min_fillings=min_fillings)

    first_actions = initial_state.get_possible_actions()
    assert len(first_actions) == NUM_HERBA_MYSTICA * NUM_FILLINGS

    state = initial_state.move(first_actions.pop())
    possible_actions = state.get_possible_actions()

    for _ in range(state.min_fillings - state.num_fillings):
        assert len(possible_actions) == NUM_FILLINGS
        state = state.move(possible_actions[0])
        possible_actions = state.get_possible_actions()

    for _ in range(state.max_fillings - state.num_fillings):
        assert len(possible_actions) == NUM_CONDIMENTS - NUM_HERBA_MYSTICA + NUM_FILLINGS + 1
        state.add_ingredient("Potato Salad")
        possible_actions = state.get_possible_actions()

    for _ in range(state.max_condiments - state.num_condiments):
        assert len(possible_actions)== NUM_CONDIMENTS - NUM_HERBA_MYSTICA + 1
        state.add_ingredient("Curry Powder")
        possible_actions = state.get_possible_actions()

    assert len(possible_actions) == 1
