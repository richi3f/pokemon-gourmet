__all__ = ["MonteCarloTreeSearch"]

import random
from math import log, sqrt
from time import time
from typing import Callable, Iterator, Optional, Sequence, Type, Union

from pokemon_gourmet.suggester.mcts.action import (
    Action,
    FinishSandwich,
    SelectBaseRecipe,
    SelectCondiment,
    SelectFilling,
)
from pokemon_gourmet.suggester.mcts.policies import (
    RolloutPolicy,
    random_rollout_policy,
)
from pokemon_gourmet.suggester.mcts.state import State

FilterFunction = Callable[["Node"], bool]


class Node(Sequence):
    """A node from a search tree"""

    def __init__(
        self,
        state: State,
        parent: Optional["Node"] = None,
        parent_action: Optional[Action] = None,
    ) -> None:
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children: dict[Action, Node] = {}
        self._num_visits = 0
        self._total_reward = 0.0
        self._untried_actions = self.state.get_possible_actions()

    def __getitem__(
        self, key: Union[int, str, tuple[str, str], Action, Type[FinishSandwich]]
    ) -> "Node":
        if isinstance(key, Action):
            return self.children[key]
        if isinstance(key, type) and issubclass(key, FinishSandwich):
            return self.children[FinishSandwich()]
        if isinstance(key, tuple):
            return self.children[SelectBaseRecipe(*key)]
        if isinstance(key, str):
            try:
                return self.children[SelectCondiment(key)]
            except KeyError:
                return self.children[SelectFilling(key)]
        if isinstance(key, int):
            if key >= len(self):
                raise IndexError()
            children = [*self]
            return children[key]
        raise KeyError()

    def __iter__(self) -> Iterator["Node"]:
        return iter(self.children.values())

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        s = "s" if self._num_visits != 1 else ""
        return f"State({self._num_visits} visit{s}, {self._total_reward:.3f} reward)"

    def __str__(self) -> str:
        return (
            f"State: {self.state}\nNumber of visits: {self._num_visits}\n"
            f"Total reward: {self._total_reward:.3f}"
        )

    @property
    def is_fully_expanded(self) -> bool:
        """A node is fully-expanded if it runs out of untried actions."""
        return len(self._untried_actions) == 0

    @property
    def is_terminal_node(self) -> bool:
        return self.state.is_terminal

    @property
    def untried_actions(self) -> list[Action]:
        return self._untried_actions

    def backpropagate(self, reward: float) -> None:
        """Update the number of visits and total reward statistics until the
        root node is reached."""
        self._num_visits += 1
        self._total_reward += reward
        if self.parent is not None:
            self.parent.backpropagate(reward)

    def expand(self) -> "Node":
        """From the present state, generate a next state based on a random
        untried action."""
        idx = random.randint(0, len(self._untried_actions) - 1)
        action = self._untried_actions.pop(idx)
        next_state = self.state.move(action)
        child_node = Node(next_state, self, action)
        self.children[action] = child_node
        return child_node

    def get_leaves(
        self, filter_func: Optional[FilterFunction] = None
    ) -> Iterator["Node"]:
        """Yield all succesors that are terminal nodes."""
        stack = [self]
        while stack:
            node = stack.pop()
            if node.is_terminal_node and (filter_func is None or filter_func(node)):
                yield node
            for child in node.children.values():
                stack.append(child)

    def reset_node(self) -> None:
        """Clear a node's total reward and number of visits, but keep edges."""
        self._total_reward = 1e-8
        self._num_visits = 1
        for child in self:
            child.reset_node()


class MonteCarloTreeSearch:
    """An optimizer based on the Monte Carlo tree search (MCTS) algorithm.

    MCTS explores a branching decision landscape. Each decision (an action)
    offers a reward, which biases the algorithm towards the selection of paths
    that maximize this reward.

    MCTS consits of four steps: selection, expansion, rollout, and
    backpropagation.

    1. Selection. Traverse the tree until reaching a leaf node. Trajectory is
    based on each node's weighted score (upper confidence bounds on trees, UCT).
    2. Expansion. If the selected leaf node can be expanded, expand it by
    selecting a random untried action and generating a child.
    3. Rollout. From the previous node, use the rollout policy to select legal
    actions until a terminal node is reached.
    4. Backpropagation. Update the parent nodes with the result from the
    rollout.

    Args:
        initial_state: Initial state
        rollout_policy: Policy used to decide which actions to take
        exploration_constant: Bias towards exploration of untried actions
        max_walltime: Maximum time to perform the rollout step
    """

    def __init__(
        self,
        initial_state: State,
        rollout_policy: RolloutPolicy = random_rollout_policy,
        exploration_constant: float = 1 / sqrt(2),
        max_walltime: int = 1000,
    ) -> None:
        self.rollout_policy = rollout_policy
        self.exploration_constant = exploration_constant
        self.max_walltime = max_walltime
        self.root = Node(initial_state)

    def __repr__(self) -> str:
        return self.__class__.__name__

    def rollout(self, node: Node) -> float:
        """Simulate a game until there is an outcome."""
        current_rollout_state = node.state
        while not current_rollout_state.is_terminal:
            action = self.rollout_policy(current_rollout_state)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.get_reward()

    def select_node(self, current_node: Node) -> Node:
        """Select node to rollout."""
        while not current_node.is_terminal_node:
            if current_node.is_fully_expanded:
                current_node = self.select_child(current_node)
            else:
                return current_node.expand()
        return current_node

    def select_child(self, parent: Node) -> Node:
        """Draw child node sample according to UCT."""
        children = [*parent.children.values()]
        weights = []
        for child in children:
            score = child._total_reward / child._num_visits
            uct = score + self.exploration_constant * sqrt(
                2 * log(parent._num_visits) / child._num_visits
            )
            weights.append(uct)
        return random.choices(children, weights, k=1)[0]

    def search(self, parent: Node) -> Node:
        """Return the node corresponding to the best possible move."""
        max_walltime = time() + self.max_walltime / 1000
        while time() < max_walltime:
            node = self.select_node(parent)
            reward = self.rollout(node)
            node.backpropagate(reward)
        best_child = self.select_best_child(parent)
        return best_child

    def select_best_child(self, parent: Node) -> Node:
        """Select the node's best child."""
        max_score = float("-inf")
        best_children: list[Node] = []
        for child in parent.children.values():
            score = child._total_reward / child._num_visits
            if score > max_score:
                max_score = score
                best_children = [child]
            elif score == max_score:
                best_children.append(child)
        if len(best_children) > 1:
            return random.choice(best_children)
        return best_children[0]
