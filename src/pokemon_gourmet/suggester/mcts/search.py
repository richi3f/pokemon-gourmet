__all__ = ["MonteCarloTreeSearch"]

import random
from math import log, sqrt
from time import time
from typing import Optional

from pokemon_gourmet.suggester.mcts.action import Action
from pokemon_gourmet.suggester.mcts.policies import (
    RolloutPolicy,
    random_rollout_policy,
)
from pokemon_gourmet.suggester.mcts.state import State


class Node:
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

    @property
    def is_fully_expanded(self):
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
        """From the present state, generate a next state based on the next
        untried action."""
        idx = random.randint(0, len(self._untried_actions) - 1)
        action = self._untried_actions.pop(idx)
        next_state = self.state.move(action)
        child_node = Node(next_state, self, action)
        self.children[action] = child_node
        return child_node

    def __repr__(self) -> str:
        s = "s" if self._num_visits != 1 else ""
        return f"State({self._num_visits} visit{s}, {self._total_reward} reward)"

    def __str__(self) -> str:
        return (
            f"State: {self.state}\nNumber of visits: {self._num_visits}\n"
            f"Total reward: {self._total_reward}"
        )


class MonteCarloTreeSearch:
    def __init__(
        self,
        rollout_policy: RolloutPolicy = random_rollout_policy,
        exploration_constant: float = 1 / sqrt(2),
        max_walltime: int = 1000,
    ) -> None:
        self.rollout_policy = rollout_policy
        self.exploration_constant = exploration_constant
        self.max_walltime = max_walltime

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
                current_node = self.best_child(current_node, self.exploration_constant)
            else:
                return current_node.expand()
        return current_node

    def search(self, initial_state: State) -> Node:
        """Return the node corresponding to the best possible move."""
        root = Node(initial_state)
        max_walltime = time() + self.max_walltime / 1000
        while time() < max_walltime:
            node = self.select_node(root)
            reward = self.rollout(node)
            node.backpropagate(reward)
        best_child = self.best_child(root, 0)
        return best_child

    def best_child(self, node: Node, exploration_constant: float) -> Node:
        """Select the node's best child."""
        max_uct = float("-inf")
        best_children: list[Node] = []
        for child in node.children.values():
            uct = child._total_reward / child._num_visits
            uct += exploration_constant * sqrt(
                2 * log(node._num_visits) / child._num_visits
            )
            if uct > max_uct:
                max_uct = uct
                best_children = [child]
            elif uct == max_uct:
                best_children.append(child)
        if len(best_children) > 1:
            return random.choice(best_children)
        return best_children[0]

    def __repr__(self) -> str:
        return self.__class__.__name__
