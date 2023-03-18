__all__ = ["recipe_generator", "validate_targets"]

from typing import Any, Iterable, Iterator, Union

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.effect import Effect, EffectList, EffectTuple
from pokemon_gourmet.suggester import exceptions as e
from pokemon_gourmet.suggester.mcts.search import MonteCarloTreeSearch
from pokemon_gourmet.suggester.mcts.state import Sandwich, State

CouldBeTarget = Union[Effect, EffectTuple, Iterable[str]]


def parse_targets(putative_targets: Iterable[CouldBeTarget]) -> EffectList:
    targets = []
    for effect in putative_targets:
        power, type_, *_ = effect
        if isinstance(power, str):
            power = Power[power.upper()]
        if isinstance(type_, str):
            type_ = Type[type_.upper()]
        targets.append((power, type_, None))
    return EffectList(targets)


def validate_targets(targets: EffectList) -> None:
    """Check that a sandwich's desired effects are valid.

    Args:
        targets: list of desired sandwich effects

    Raises:
        RepeatedPowers:
            If sandwich has two or more effects with the same type of Power
        InvalidEffects:
            If Sparkling Power and Title Power are not paired
        TypedEggPower:
            If Egg Power is not typeless
    """
    if len(targets.powers) != len(targets):
        raise e.RepeatedPowers(
            "Repeated powers. A sandwich cannot have two or more of the same effect."
        )
    if Power.SPARKLING in targets.powers and not Power.TITLE in targets.powers:
        raise e.InvalidEffects(
            "Invalid effects. Sparkling Power is always paired with Title Power."
        )
    if Power.EGG in targets.powers and (Power.EGG, None) not in targets:
        raise e.TypedEggPower("Invalid effect. Egg Power should be typeless.")


def recipe_generator(
    targets: Iterable[CouldBeTarget], max_iter: int, mcts_kwargs: dict[str, Any]
) -> Iterator[State]:
    """Run MCTS to generate sandwich recipes that meet the target effects.

    Args:
        targets: Desired effects in suggested sandwich recipes
        max_iter: Number of times to run the MCTS
        mcts_kwargs: Arguments to initialize the MCTS object

    Yields:
        Sandwiches
    """
    # Validate input
    i = 0
    targets = parse_targets(targets)
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
