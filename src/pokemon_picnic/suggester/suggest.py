__all__ = ["suggest"]

from typing import Any, Iterator, Sequence

from pokemon_picnic.suggester.exceptions import RepeatedPowers
from pokemon_picnic.suggester.mcts.search import MonteCarloTreeSearch
from pokemon_picnic.suggester.mcts.state import Sandwich, State, Target


def validate_targets(targets: Sequence[Target]) -> None:
    powers = set([target.power for target in targets])
    if len(powers) != 3:
        raise RepeatedPowers("Cannot repeat any power.")


def suggest(
    targets: Sequence[Target], max_iter: int, mcts_kwargs: dict[str, Any]
) -> Iterator[State]:
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
