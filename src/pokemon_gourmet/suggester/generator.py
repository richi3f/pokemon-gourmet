__all__ = ["parse_targets", "RecipeGenerator", "validate_targets"]

from operator import attrgetter
from typing import Any, Iterable, Iterator, Union, cast

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.effect import Effect, EffectList, EffectTuple
from pokemon_gourmet.sandwich.recipe import MAX_FILLINGS
from pokemon_gourmet.suggester.exceptions import InvalidEffects
from pokemon_gourmet.suggester.mcts.search import MonteCarloTreeSearch
from pokemon_gourmet.suggester.mcts.state import RecipeManager, RecipeState

CouldBeTarget = Union[Effect, EffectTuple, Iterable[str]]


def parse_targets(putative_targets: Iterable[CouldBeTarget]) -> EffectList:
    """Return an effect list from a list of putative effects.

    Args:
        putative_targets:
            List of `pokemon_gourmet.sandwich.effect.Effect` instances, tuples
            of `pokemon_gourmet.enums.Power` and `pokemon_gourmet.enums.Type`,
            or tuples containing one string corresponding to Power and one
            string corresponding to a Pokémon Type

    Returns:
        Effect list
    """
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
        InvalidEffects:
            If sandwich has two or more effects with the same type of Power.

            If Sparkling Power and Title Power are not paired.

            If Sparkling Power is present and not all Types are the same.

            If Sparkling Power is not present and all Types are the same.

            If there is a typeless effect that is not Egg Power.

            If Egg Power is not typeless.
    """
    if len(targets.powers) != len(targets):
        raise InvalidEffects(
            "A sandwich cannot have two or more effects sharing the same type of Power."
        )
    have_egg_power = Power.EGG in targets
    if have_egg_power and (Power.EGG, None) not in targets:
        raise InvalidEffects("Egg Power should be typeless.")
    if Power.SPARKLING in targets:
        if Power.TITLE not in targets:
            raise InvalidEffects("Sparkling Power is always paired with Title Power.")
        if len(targets.types) > (1 + have_egg_power):
            raise InvalidEffects(
                "If Sparkling Power is present, every Type must be the same."
            )
    elif len(targets) == 3 and not have_egg_power and len(targets.types) == 1:
        # Only true for single-player
        raise InvalidEffects(
            "Sparkling Power is required for all Powers to share Type."
        )
    if any(
        effect.pokemon_type is None for effect in targets if effect.power == Power.EGG
    ):
        raise InvalidEffects("No effect (other than Egg Power) should be typeless.")


class RecipeGenerator(Iterator[list[RecipeState]]):
    """Use Monte Carlo tree search to explore ingredient combinations and
    generate recipes that match the target effects.

    Args:
        targets: Desired effects on the output sandwich recipes
        num_iter: Number of times to explore the search tree
        min_fillings: Minimum number of fillings to include in recipe
        max_fillings: Maximum number of fillings to include in recipe
    """

    def __init__(
        self,
        targets: Iterable[CouldBeTarget],
        num_iter: int,
        min_fillings: int = 1,
        max_fillings: int = MAX_FILLINGS,
        **mcts_kwargs: Any,
    ) -> None:
        self.targets = parse_targets(targets)
        validate_targets(self.targets)
        self.it = 0
        self.num_iter = num_iter
        self.mcts_kwargs = mcts_kwargs
        initial_state = RecipeState(self.targets, min_fillings, max_fillings)
        self.mcts = MonteCarloTreeSearch(
            initial_state, RecipeManager(), **self.mcts_kwargs
        )
        self.saved_results = set()

    def _search(self) -> None:
        node = self.mcts.root
        if node._num_visits > 0:
            node.reset_node()
        while not node.is_terminal_node:
            node = self.mcts.search(node)
            assert node.parent_action is not None
            node.state.move(node.parent_action)

    def __next__(self) -> list[RecipeState]:
        if self.it >= self.num_iter:
            raise StopIteration
        self.it += 1
        self._search()
        # Filter recipes (a recipe state evaluates to True if it's a match)
        states = [
            node.state
            for node in self.mcts.root.get_leaves(attrgetter("state"))
            if node.state not in self.saved_results
        ]
        self.saved_results.update(states)
        return cast(list[RecipeState], states)

    def __iter__(self) -> "RecipeGenerator":
        self.it = 0
        return self
