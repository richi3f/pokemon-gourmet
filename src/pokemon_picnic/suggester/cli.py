from math import sqrt

import click

from pokemon_picnic.core.enums import Power, Type
from pokemon_picnic.suggester.mcts.search import MonteCarloTreeSearch
from pokemon_picnic.suggester.mcts.state import Sandwich, Target


def parse_targets(targets_str: tuple[str, ...]) -> list[Target]:
    """Parse and validate a string of target effects.

    Args:
        targets_str:
            A target as a string. Each target consists of a power and Pokémon
            type separated by a comma (except in the case of the Egg power,
            which is typeless).

    Raises:
        ValueError: If the target effect is incorrectly formatted
        ValueError: If a power repeats

    Returns:
        List of target effects (power-type combo)
    """
    targets = []
    powers = set()
    for target_str in targets_str:
        if "egg" in target_str.lower():
            power = Power.EGG
            pokemon_type = None
        else:
            power_str, type_str, *_ = target_str.split(",")
            if len(_) > 0:
                raise ValueError(
                    "Incorrectly formatted effect. "
                    f"Input ('{target_str}') should only have one comma, "
                    "separating power and Pokémon type (e.g., 'teensy,fairy')."
                )
            power = Power[power_str.upper()]
            pokemon_type = Type[type_str.upper()]
        effect = Target(power, pokemon_type)
        targets.append(effect)
        powers.add(power)
    if len(powers) != 3:
        raise ValueError("Cannot repeat any power.")
    return targets


@click.command()
@click.argument("targets_str", nargs=3, type=str)
@click.option("-c", "--exploration-constant", default=1 / sqrt(2), type=float)
@click.option("-w", "--max-walltime", default=1000, type=int)
def suggest(
    targets_str: tuple[str, str, str],
    exploration_constant: float,
    max_walltime: int,
):
    targets = parse_targets(targets_str)

    current_state = Sandwich(targets)
    mcts = MonteCarloTreeSearch(
        exploration_constant=exploration_constant,
        max_walltime=max_walltime,
    )
    # Run game until a solution is found
    while not current_state.is_terminal:
        node = mcts.search(current_state)
        assert node.parent_action is not None
        current_state = current_state.move(node.parent_action)
    print(getattr(current_state, "ingredients"))


if __name__ == "__main__":
    suggest()
