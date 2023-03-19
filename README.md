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

To get a sandwich recipe from the command line, run the `gourmet`command.

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
suggester = RecipeGenerator(desired_effects, 10)
recipes = [recipe for recipe in suggester]
```

Pass effects as pairs of a Power and a Pokémon Type. These can be
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
intractable amount of combinations (probably more than 30 quadrillion recipes!).

:sandwich: Cue MCTS, an exploratory algorithm that can smartly traverse through
a landscape of branching decision landscape, weigh each decision, and select
the most profitable decision path. In the context of sandwich making, a decision
refers to adding an ingredient to a sandwich's recipe. Each decision is scored
based on how it affects the sandwich's effects and its match to the user-input
desired effects. The most profitable decision path then reads like a sandwich
recipe .

### Configuration

- `num_trees` (`n` in CLI) - number of trees to grow and explore. Each tree is
  a new instance of the search algorithm.

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
  - `weighted_allocator` - assigns a weight to each ingredient based on the
    free space in the sandwich. This intends to balance the number of fillings
    and condiments in the sandwich.

#### Examples:

Attempt to generate a recipe with an exploration constant of 5 and only 100 ms
to select each ingredient (note this is a very short time, it may not find a
solution).

```bash
gourmet title,fairy encounter,fairy humungo,ghost -c 5 -w 100
```

Attempt to generate a recipe using the short recipe rollout policy with a 50%
chance to finish the recipe early.

```bash
gourmet title,bug encounter,bug teensy,water -r early_stopping --prob 0.5
```

Grow and explore 10 trees using the weighted allocator rollout policy.

```python
from functools import partial
from pokemon_gourmet import RecipeGenerator
from pokemon_gourmet.suggester.mcts import ROLLOUT_POLICIES

rollout_policy = partial(
    ROLLOUT_POLICIES["weighted_allocator"],
    finish_prob=0.05
)

suggester = RecipeGenerator(
    desired_effects,
    num_trees=10,
    max_walltime=1000,
    rollout_policy=rollout_policy,
)
recipes = [recipe for recipe in suggester]
```

## Remarks

<dl>
<dt>Are all effect combinations possible?</dt>
<dd>No. The algorithm is aware of some impossible combinations, so it will not
run if you ask, for instance, for a sandwich that has Sparkling Power but no
Title Power. However, other combinations might be impossible and the algorithm
will still run and try to find the closest match (i.e., either one or two
matching effects).</dd>
<dt>Why did it not find any recipe matching my target effects?</dt>
<dd>The search process is stochastic, so there is no guarantee that two searches
will have the same results. For this reason, I recommend setting the
<code>num_trees</code> argument to 10 or more. This should result in at least a
couple of recipes that match your target effects. Also, increase the
<code>max_walltime</code> to give time to the searcher to explore the decision
landscape.</dd>
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