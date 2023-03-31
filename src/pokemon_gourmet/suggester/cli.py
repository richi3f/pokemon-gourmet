__all__ = []

import inspect
from collections import Counter
from functools import partial
from math import sqrt
from pathlib import Path

import click
import numpy as np
import pandas as pd

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.effect import EffectTuple
from pokemon_gourmet.sandwich.recipe import MAX_CONDIMENTS, MAX_FILLINGS
from pokemon_gourmet.suggester.generator import RecipeGenerator
from pokemon_gourmet.suggester.mcts import policies as p
from pokemon_gourmet.suggester.mcts.state import Sandwich


def parse_targets(targets_str: tuple[str, ...]) -> list[EffectTuple]:
    """Parse and validate a string of target effects.

    Args:
        targets_str:
            A target as a string. Each target consists of a power and Pokémon
            type separated by a comma (except in the case of the Egg Power,
            which is typeless).

    Raises:
        ValueError: If the target effect is incorrectly formatted

    Returns:
        List of target effects (Power-Type combo)
    """
    targets = []
    for i, target_str in enumerate(targets_str):
        if i >= 3:
            raise ValueError("Maximum three target effects permitted.")
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
    return targets


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


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("targets_str", nargs=-1, type=str)
@click.option(
    "-n",
    "--num-iter",
    default=10,
    type=int,
    help="Number of times to explore the search tree",
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
    targets = parse_targets(targets_str)
    rollout_policy_func = parse_rollout_policy(rollout_policy, ctxt.args)

    print("Looking for sandwiches, please wait…\n")
    mcts_kwargs = dict(
        rollout_policy=rollout_policy_func,
        exploration_constant=exploration_constant / sqrt(2),
        max_walltime=max_walltime,
    )
    recipe_gen = RecipeGenerator(targets, num_iter, **mcts_kwargs)

    unique_recipes: set[Sandwich] = set()
    for recipes in recipe_gen:
        if not recipes:
            continue
        unique_recipes.update(recipes)

    rows = []
    for recipe in unique_recipes:
        condiments = recipe.condiments
        fillings = recipe.fillings
        effects = recipe.effects.tuples
        rows.append(
            (
                *effects,
                *fillings,
                *[""] * (recipe.max_fillings - len(fillings)),
                *condiments,
                *[""] * (recipe.max_condiments - len(condiments)),
                recipe.reward,
                -len(fillings),
                -len(condiments),
                -recipe.total_pieces,
            )
        )

    save_path = Path.cwd() / "recipes.csv"
    sorting_columns = ["score", "num_fillings", "total_pieces", "num_condiments"]
    df = pd.DataFrame(
        rows,
        columns=[
            *[f"effect{i + 1}" for i in range(3)],
            *[f"filling{i + 1}" for i in range(MAX_FILLINGS)],
            *[f"condiment{i + 1}" for i in range(MAX_CONDIMENTS)],
            *sorting_columns,
        ],
    ).sort_values(sorting_columns, ascending=False)
    df["score"] = np.round(df["score"], 3)
    df.drop(sorting_columns[1:], axis=1, inplace=True)
    df.to_csv(save_path, index=False)

    s = "s" if len(df) != 1 else ""
    print(f"Found {len(df)} recipe{s}!\nSaved results to: {save_path}")

if __name__ == "__main__":
    main()
