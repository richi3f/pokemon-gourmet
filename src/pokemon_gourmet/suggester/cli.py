__all__ = []

import inspect
from collections import Counter
from functools import partial
from math import sqrt
from operator import methodcaller

import click

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.effect import EffectList
from pokemon_gourmet.sandwich.ingredient import Ingredient
from pokemon_gourmet.suggester.generator import RecipeGenerator
from pokemon_gourmet.suggester.mcts import policies as p


def parse_targets(targets_str: tuple[str, ...]) -> EffectList:
    """Parse and validate a string of target effects.

    Args:
        targets_str:
            A target as a string. Each target consists of a power and Pokémon
            type separated by a comma (except in the case of the Egg Power,
            which is typeless).

    Raises:
        ValueError: If the target effect is incorrectly formatted

    Returns:
        List of target effects (power-type combo)
    """
    targets = []
    for target_str in targets_str:
        if "egg" in target_str.lower():
            power = Power.EGG
            pokemon_type = None
        else:
            if target_str.count(",") != 1:
                raise ValueError(
                    "Incorrectly formatted effect. "
                    f"Input ('{target_str}') should contain one comma "
                    "separating Power and Pokémon Type (e.g., 'teensy,bug')."
                )
            power_str, type_str = target_str.split(",")
            power = Power[power_str.upper()]
            pokemon_type = Type[type_str.upper()]
        targets.append((power, pokemon_type))
    return EffectList(targets)


def parse_rollout_policy(func_name: str, ctxt_args: list[str]) -> p.RolloutPolicy:
    """Parse rollout policy and its corresponding keyword arguments from
    click's context."""
    func = p.ROLLOUT_POLICIES[func_name]
    params = inspect.signature(func).parameters
    if len(params) > 1:
        func_kwargs = {}
        ctxt_kwargs = {
            ctxt_args[i].strip("--"): ctxt_args[i + 1]
            for i in range(0, len(ctxt_args), 2)
        }
        for parameter in params.values():
            if parameter.name == "state":
                continue
            if parameter.name not in ctxt_kwargs:
                continue
            func_kwargs[parameter.name] = parameter.annotation(
                ctxt_kwargs[parameter.name]
            )
        func = partial(func, **func_kwargs)
    return func


def format_ingredients(ingredients: list[Ingredient]) -> str:
    """Format list of ingredients."""
    counts = Counter(ingredients)
    return "\n- " + "\n- ".join(
        f"{ingredient.name}" + (f" (x{count})" if count > 1 else "")
        for ingredient, count in counts.most_common()
    )


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("targets_str", nargs=3, type=str)
@click.option(
    "-n",
    "--num-iter",
    default=10,
    type=int,
    help="Number of times to explore the decision tree",
)
@click.option(
    "-r",
    "--rollout-policy",
    default="random",
    type=str,
    help="Policy used to select ingredients",
)
@click.option(
    "-c",
    "--exploration-constant",
    default=1,
    type=float,
    help="Bias towards exploration of less tried ingredients",
)
@click.option(
    "-w",
    "--max-walltime",
    default=1000,
    type=int,
    help="Maximum time (in ms) to select an ingredient",
)
@click.pass_context
def main(
    ctxt: click.Context,
    targets_str: tuple[str, str, str],
    num_iter: int,
    rollout_policy: str,
    exploration_constant: float,
    max_walltime: int,
):
    if len(targets_str) != 3:
        raise ValueError("Three desired effects must be specified.")
    targets = parse_targets(targets_str)
    rollout_policy_func = parse_rollout_policy(rollout_policy, ctxt.args)

    print("Looking for sandwiches, please wait…\n")
    mcts_kwargs = dict(
        rollout_policy=rollout_policy_func,
        exploration_constant=exploration_constant / sqrt(2),
        max_walltime=max_walltime,
    )
    recipe_gen = RecipeGenerator(targets, num_iter, **mcts_kwargs)

    unique_recipes = set()
    for recipes in recipe_gen:
        if not recipes:
            continue
        unique_recipes.update(recipes)

    for recipe in sorted(unique_recipes, key=methodcaller("get_reward"), reverse=True):
        filling_names = format_ingredients(getattr(recipe, "fillings"))
        condiment_names = format_ingredients(getattr(recipe, "condiments"))

        print(
            f"{recipe}\nMatch: {min(1.0, recipe.get_reward()):.3f}\n"
            f"Fillings:{filling_names}\nCondiments:{condiment_names}"
        )


if __name__ == "__main__":
    main()
