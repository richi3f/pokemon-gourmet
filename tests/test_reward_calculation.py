from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich import Effect, EffectList, Recipe
from pokemon_gourmet.suggester.mcts.state import REWARD_GROWTH_FACTOR, RecipeState

def test_1target_reward():
    desired_effects = EffectList(
        [(Power.CATCHING, Type.DRAGON)]
    )

    state = RecipeState(desired_effects)
    for ingredient in ["Avocado", "Whipped Cream"]:
        state.add_ingredient(ingredient)

    # Meal Power Level 1
    assert state.reward == 1.0

    # Meal Powers Level 2
    state.add_ingredient("Avocado")
    state.add_ingredient("Sweet Herba Mystica")
    expected_reward = 2 ** (REWARD_GROWTH_FACTOR * 1)
    assert abs(state.reward - expected_reward) < 1e-3

    # Meal Powers Level 3
    state.add_ingredient("Sour Herba Mystica")
    assert abs(state.reward - 300.0) < 1e-3


def test_2target_reward():
    desired_effects = EffectList(
        [(Power.TITLE, Type.NORMAL), (Power.TEENSY, Type.NORMAL)]
    )

    state = RecipeState(desired_effects)
    for ingredient in ["Fried Fillet", "Sour Herba Mystica"]:
        state.add_ingredient(ingredient)

    # only one Meal Power matches
    assert state.reward == 0.5

    # both Meal Powers at Level 2
    state.add_ingredient("Chorizo")
    expected_reward = 2 ** (REWARD_GROWTH_FACTOR * 1)
    assert abs(state.reward - expected_reward) < 1e-3

    # both Meal Powers at Level 3
    state.add_ingredient("Sour Herba Mystica")
    assert abs(state.reward - 300.0) < 1e-3


def test_3target_reward():
    desired_effects = EffectList(
        [
            (Power.TITLE, Type.FAIRY),
            (Power.HUMUNGO, Type.FAIRY),
            (Power.ENCOUNTER, Type.GHOST),
        ]
    )

    state = RecipeState(desired_effects)
    for ingredient in [*["Potato Salad"] * 3, "Tomato", "Spicy Herba Mystica"]:
        state.add_ingredient(ingredient)

    # every Meal Power has Level 2
    expected_reward = 2 ** (REWARD_GROWTH_FACTOR * 1)
    assert abs(state.reward - expected_reward) < 1e-3

    # Meal Powers have Levels 3, 3, and 2
    state.add_ingredient("Potato Salad")
    expected_reward = 2 ** (REWARD_GROWTH_FACTOR * 5 / 3)
    assert abs(state.reward - expected_reward) < 1e-3

    # every Meal Power has Level 3
    state.add_ingredient("Potato Salad")
    assert abs(state.reward - 300.0) < 1e-3
