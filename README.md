# :sandwich: Pokémon Gourmet

A tool to generate sandwich recipes for Pokémon Scarlet &amp; Pokémon Violet

## Installation

Clone repo and install by typing:

```bash
pip install -e .
```

Note: I recommend to install on its own virtual environment (create one with
Conda or similar). This package requires Python 3.9.

## How to run

To get sandwich recipes from the command line, run the `gourmet` command.

```bash
gourmet title,fairy encounter,fairy humungo,ghost
```

To open the graphical interface, run `gourmet-gui` command on the command line.

You can also run it in a script or Jupyter notebook. An example:

```python
from pokemon_gourmet import RecipeGenerator

desired_effects = [
  ("TITLE", "FAIRY"),
  ("ENCOUNTER", "FAIRY"),
  ("HUMUNGO", "GHOST"),
 ]
suggester = RecipeGenerator(desired_effects)
suggestions = [recipe for recipes in suggester for recipe in recipes]
```

Write effects as pairs of an effect Power and a Pokémon Type. These can be
case-insensitive strings or enums from the `pokemon_gourmet.enums` module. If
the Power is Egg Power, set Pokémon Type to `None`.

```python
from pokemon_gourmet.enums import Power

desired_effects = [
  ("Exp_Point", "bug"),
  ("item_drop", "Water"),
  (Power.EGG, None),
 ]
 ```

## About the algorithm

:deciduous_tree: This tool solves a combinatorial problem with a reinforcement
learning algorithm known as
[Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
(MCTS).

:tomato: :salt: Sandwich recipes consist of up to six fillings and four
condiments. In total, there's 58 ingredients to combine, leading to an
intractable amount of combinations (probably more than 1 trillion recipes!).

:sandwich: Cue MCTS, an exploratory algorithm that can traverse a landscape of
branching decisions, weigh each decision, and select the most profitable
decision path. In the context of sandwich making, a decision refers to adding
an ingredient to a sandwich recipe. Each decision is scored based on how it
affects the sandwich's effects and its match to the user-input desired effects.
The most profitable decision path then reads like a sandwich recipe. Yum!

### Configuration

- `num_iter` (`n` in CLI) - number of times to explore the search tree. Each
  iteration may adventure into new paths.

- `exploration_constant` (`c` in CLI) - bias of the algorithm towards
  exploration of less tried ingredients.

- `max_walltime` (`w` in CLI) - max time (in ms) the algorithm has to select an
  ingredient to add to the sandwich. The maximum time the algorithm can spend
  generating a sandwich will be this number times ten, but shorter recipes will
  take less time.

- `rollout_policy` (`r` in CLI) - policy used to choose an ingredient to add
  to the recipe. Possible policies:

  - `random` - randomly picks any ingredient.
  - `early_stopping` - favors short recipes by having a high chance of stopping
    the sandwich recipe at the earliest possibility.
  - `weighted_allocation` - assigns a weight to each ingredient based on the
    free space in the sandwich. This attempts to balance the number of fillings
    and condiments in the sandwich.

#### Examples:

Attempt to generate recipes with an exploration constant of 5 and only 100 ms
to select each ingredient (note this is a very short time, it may not find a
solution).

```bash
gourmet title,fairy encounter,fairy humungo,ghost -c 5 -w 100
```

Attempt to generate recipes using the early stopping rollout policy with a 50%
chance to finish the recipe at the earliest possible.

```bash
gourmet title,bug encounter,bug teensy,water -r early_stopping --stop_prob 0.5
```

Run the search algorithm 10 times using the weighted allocation rollout policy.

```python
from functools import partial
from pokemon_gourmet import RecipeGenerator
from pokemon_gourmet.suggester.mcts import ROLLOUT_POLICIES

rollout_policy = partial(
    ROLLOUT_POLICIES["weighted_allocation"],
    stop_prob=0.05
)

suggester = RecipeGenerator(
    desired_effects,
    num_iter=10,
    max_walltime=1000,
    rollout_policy=rollout_policy,
)
suggestions = [recipe for recipes in suggester for recipe in recipes]
```

## Remarks

<dl>
<dt>Are all effect combinations possible?</dt>
<dd>No. The algorithm is aware of some impossible combinations, so it will not
run if you ask, for instance, for a sandwich that has Sparkling Power but no
Title Power. However, other combinations might be impossible and the algorithm
will still run and try to find the closest match (i.e., either one or two
matching effects).</dd>
<dt>Why am I getting different results every time?</dt>
<dd>The search process is stochastic, so there is no guarantee that two
searches will render the same results.</dd>
<dt>What are some of the limitations of this tool?</dt>
<dd>
  <ol>
    <li>It only generates three-star sandwich recipes (i.e., it assumes no
        ingredient will fall out of the sandwich).</li>
    <li>Users can only input desired Meal Power and Type. Level cannot be
        specified, but the algorithm will still try to maximize it.</li>
    <li>Only works for single-player recipes.</li>
  </ol>
</dd>
</dl>

## Contribute

:bug: :bulb: Feel free to
[open an issue](https://github.com/richi3f/pokemon-gourmet/issues/new/choose)
if you have feedback or find a bug in the code.


## Credits

This tool would not be possible without the
[Pokémon Sandwich Simulator](https://github.com/cecilbowen/pokemon-sandwich-simulator)
from [@cecilbowen](https://github.com/cecilbowen).

Pokémon is © of Nintendo, 1995-2023.