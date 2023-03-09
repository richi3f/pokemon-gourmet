from pokemon_picnic.core.enums import Power, Type
from pokemon_picnic.sandwich import Effect, Recipe


def test_herba_mystica_recipes():
    recipe = Recipe.from_str(*["Rice"] * 5, "Bitter Herba Mystica")
    effects = recipe.effects
    assert effects[0] == Effect(Power.TITLE, Type.NORMAL, 3)
    assert effects[1] == Effect(Power.HUMUNGO, Type.NORMAL, 3)
    assert effects[2] == Effect(Power.ITEM_DROP, Type.FLYING, 3)

    recipe = Recipe.from_str(*["Rice"] * 4, "Bitter Herba Mystica")
    effects = recipe.effects
    assert effects[0] == Effect(Power.TITLE, Type.NORMAL, 2)
    assert effects[1] == Effect(Power.ITEM_DROP, Type.NORMAL, 2)
    assert effects[2] == Effect(Power.HUMUNGO, Type.FLYING, 2)

    recipe = Recipe.from_str(
        *["Herbed Sausage"] * 2, *["Rice"] * 2, "Horseradish", "Spicy Herba Mystica"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.TITLE, Type.FIGHTING, 3)
    assert effects[1] == Effect(Power.HUMUNGO, Type.FIGHTING, 3)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.GROUND, 2)


def test_non_herba_mystica_recipes():
    recipe = Recipe.from_str(*["Rice"] * 6, *["Wasabi"] * 2, *["Curry Powder"] * 2)
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.FIRE, 2)
    assert effects[1] == Effect(Power.HUMUNGO, Type.GRASS, 2)
    assert effects[2] == Effect(Power.RAID, Type.WATER, 1)

    recipe = Recipe.from_str(
        *["Chorizo"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, "Pepper", "Curry Powder"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        *["Chorizo"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.BUG, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        *["Chorizo"] * 4, *["Wasabi"] * 2, "Rice", "Potato Salad", *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.BUG, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.FIRE, 1)

    recipe = Recipe.from_str(
        *["Fried Fillet"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.WATER, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.FLYING, 1)
    assert effects[2] == Effect(Power.TEENSY, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        *["Fried Fillet"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.WATER, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.FLYING, 1)
    assert effects[2] == Effect(Power.TEENSY, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        "Potato Tortilla",
        "Potato Tortilla",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Curry Powder",
        "Curry Powder",
        "Wasabi",
        "Wasabi",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.FIRE, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.FIGHTING, 1)
    assert effects[2] == Effect(Power.HUMUNGO, Type.GRASS, 1)

    recipe = Recipe.from_str("Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Wasabi")
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect(Power.RAID, Type.FLYING, 2)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.FIGHTING, 1)

    recipe = Recipe.from_str(
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Salt",
        "Salt",
        "Vinegar",
        "Vinegar",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.FLYING, 2)
    assert effects[2] == Effect(Power.TEENSY, Type.FIGHTING, 1)

    recipe = Recipe.from_str(
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Curry Powder",
        "Curry Powder",
        "Olive Oil",
        "Wasabi",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.WATER, 2)
    assert effects[2] == Effect(Power.RAID, Type.GRASS, 1)

    recipe = Recipe.from_str(
        "Sliced Egg",
        "Sliced Egg",
        "Sliced Egg",
        "Jalapeno",
        "Jalapeno",
        "Potato Salad",
        "Whipped Cream",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.FAIRY, 2)
    assert effects[1] == Effect(Power.EXP_POINT, Type.GRASS, 1)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.ROCK, 1)

    recipe = Recipe.from_str(
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Chili Sauce",
        "Chili Sauce",
        "Cream Cheese",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.WATER, 2)
    assert effects[1] == Effect(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.GRASS, 1)

    recipe = Recipe.from_str(
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Chili Sauce",
        "Chili Sauce",
        "Olive Oil",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.GRASS, 2)
    assert effects[1] == Effect(Power.HUMUNGO, Type.WATER, 2)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.FIRE, 1)

    recipe = Recipe.from_str(
        "Herbed Sausage",
        "Herbed Sausage",
        "Herbed Sausage",
        "Herbed Sausage",
        "Potato Tortilla",
        "Potato Tortilla",
        "Salt",
        "Yogurt",
        "Yogurt",
        "Yogurt",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.PSYCHIC, 2)
    assert effects[1] == Effect(Power.EXP_POINT, Type.GHOST, 2)
    assert effects[2] == Effect(Power.RAID, Type.FIGHTING, 1)

    recipe = Recipe.from_str(
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Rice",
        "Curry Powder",
        "Ketchup",
        "Wasabi",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.FLYING, 2)
    assert effects[1] == Effect(Power.HUMUNGO, Type.WATER, 2)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.FIRE, 1)

    recipe = Recipe.from_str(
        "Prosciutto",
        "Prosciutto",
        "Prosciutto",
        "Prosciutto",
        "Watercress",
        "Pepper",
        "Salt",
        "Salt",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.EXP_POINT, Type.FLYING, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.PSYCHIC, 1)
    assert effects[2] == Effect(Power.RAID, Type.ELECTRIC, 1)

    recipe = Recipe.from_str(
        "Prosciutto",
        "Prosciutto",
        "Prosciutto",
        "Prosciutto",
        "Watercress",
        "Watercress",
        "Pepper",
        "Salt",
        "Salt",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.EXP_POINT, Type.FLYING, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.FIGHTING, 1)
    assert effects[2] == Effect(Power.RAID, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        "Hamburger", "Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Ketchup"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.POISON, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.STEEL, 1)

    recipe = Recipe.from_str(
        "Cheese",
        "Chorizo",
        "Chorizo",
        "Chorizo",
        "Chorizo",
        "Tofu",
        "Pepper",
        "Whipped Cream",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect(Power.EXP_POINT, Type.POISON, 1)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.DRAGON, 1)

    recipe = Recipe.from_str(
        "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Pepper", "Whipped Cream"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect(Power.RAID, Type.FIGHTING, 2)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.FLYING, 1)

    recipe = Recipe.from_str(
        "Sliced Egg",
        "Noodles",
        "Noodles",
        "Noodles",
        "Noodles",
        "Noodles",
        "Wasabi",
        "Wasabi",
        "Yogurt",
        "Yogurt",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.ICE, 2)
    assert effects[1] == Effect(Power.HUMUNGO, Type.ELECTRIC, 1)
    assert effects[2] == Effect(Power.ENCOUNTER, Type.ROCK, 1)

    recipe = Recipe.from_str("Onion", "Onion", "Onion", "Onion", "Butter")
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.PSYCHIC, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.BUG, 1)

    recipe = Recipe.from_str("Onion", "Onion", "Onion", "Onion", "Strawberry", "Salt")
    effects = recipe.effects
    assert effects[0] == Effect(Power.RAID, Type.PSYCHIC, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.FIGHTING, 1)

    """recipe = Recipe.from_str(
        ["Hamburger"] * 5, "Red Bell Pepper", "Peanut Butter", "Peanut Butter"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.FIRE, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.NORMAL, 1)"""

    recipe = Recipe.from_str(
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Kiwi",
        "Kiwi",
        "Chili Sauce",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ITEM_DROP, Type.POISON, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.FIRE, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Red Bell Pepper",
        "Butter",
        "Peanut Butter",
        "Peanut Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.BUG, 1)
    assert effects[2] == Effect(Power.RAID, Type.FIRE, 1)


def test_split_types():

    recipe = Recipe.from_str(
        "Hamburger", "Hamburger", "Hamburger", "Hamburger", "Hamburger", "Butter"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.STEEL, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.GHOST, 1)

    recipe = Recipe.from_str(
        "Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Watercress", "Salt"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.FIGHTING, 1)
    assert effects[2] == Effect(Power.RAID, Type.FLYING, 1)

    recipe = Recipe.from_str(
        "Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Ketchup"
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.NORMAL, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.FLYING, 1)

    recipe = Recipe.from_str(
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Ketchup",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ITEM_DROP, Type.POISON, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.NORMAL, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.POISON, 1)

    recipe = Recipe.from_str(
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Kiwi",
        "Ketchup",
        "Ketchup",
        "Ketchup",
        "Ketchup",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.TEENSY, Type.POISON, 1)
    assert effects[1] == Effect(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect(Power.RAID, Type.POISON, 1)

    recipe = Recipe.from_str(
        "Cheese",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.GHOST, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.STEEL, 1)

    recipe = Recipe.from_str("Ham", "Ham", "Ham", "Ham", "Mustard")
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.GROUND, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.NORMAL, 1)
    assert effects[2] == Effect(Power.EXP_POINT, Type.GROUND, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Watercress",
        "Peanut Butter",
        "Peanut Butter",
        "Peanut Butter",
        "Peanut Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.RAID, Type.NORMAL, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.STEEL, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Peanut Butter",
        "Peanut Butter",
        "Peanut Butter",
        "Peanut Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.CATCHING, Type.STEEL, 1)
    assert effects[2] == Effect(Power.RAID, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Peanut Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.NORMAL, 1)

    recipe = Recipe.from_str(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Mustard",
    )
    effects = recipe.effects
    assert effects[0] == Effect(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect(Power.CATCHING, Type.ROCK, 1)
