__all__ = ["suggest"]

from typing import Any, Iterator, Sequence

from pokemon_gourmet.core.enums import Power
from pokemon_gourmet.suggester import exceptions as e
from pokemon_gourmet.suggester.mcts.search import MonteCarloTreeSearch
from pokemon_gourmet.suggester.mcts.state import Sandwich, State, Target


def validate_targets(targets: Sequence[Target]) -> None:
    """Check that a sandwich's desired effects are valid.

    Args:
        targets: list of desired sandwich effects

    Raises:
        RepeatedPowers:
            If sandwich has two or more effects with the same type of Power
        InvalidEffects:
            If Sparkling Power and Title Power are not paired
    """
    powers = set([target.power for target in targets])
    if len(powers) != 3:
        raise e.RepeatedPowers(
            "Repeated powers. A sandwich cannot have two or more of the same effect."
        )
    if Power.SPARKLING in powers and not Power.TITLE in powers:
        raise e.InvalidEffects(
            "Invalid effects. Sparkling Power is always paired with Title Power."
        )


def suggest(
    targets: Sequence[Target], max_iter: int, mcts_kwargs: dict[str, Any]
) -> Iterator[State]:
    """Run MCTS to suggest sandwich recipes that meet the target effects.

    Args:
        targets: Desired effects in suggested sandwich recipes
        max_iter: Number of times to run the MCTS
        mcts_kwargs: Arguments to initialize the MCTS object

    Yields:
        Sandwiches
    """
    # Validate input
    i = 0
    validate_targets(targets)
    mcts = MonteCarloTreeSearch(**mcts_kwargs)
    while i < max_iter:
        current_state = Sandwich(targets)
        # Run game until a solution is found
        while not current_state.is_terminal:
            node = mcts.search(current_state)
            assert node.parent_action is not None
            current_state = current_state.move(node.parent_action)
        else:
            i += 1
            yield current_state
