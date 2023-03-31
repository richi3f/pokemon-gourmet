from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich import Effect, Recipe


def test_herba_mystica_recipes():
    recipe = Recipe(*["Rice"] * 5, "Bitter Herba Mystica")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.TITLE, Type.NORMAL, 3)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 3)
    assert effects[2] == Effect.from_enums(Power.ITEM_DROP, Type.FLYING, 3)

    recipe = Recipe(*["Rice"] * 4, "Bitter Herba Mystica")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.TITLE, Type.NORMAL, 2)
    assert effects[1] == Effect.from_enums(Power.ITEM_DROP, Type.NORMAL, 2)
    assert effects[2] == Effect.from_enums(Power.HUMUNGO, Type.FLYING, 2)

    recipe = Recipe(
        *["Herbed Sausage"] * 2, *["Rice"] * 2, "Horseradish", "Spicy Herba Mystica"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.TITLE, Type.FIGHTING, 3)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.FIGHTING, 3)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.GROUND, 2)


def test_non_herba_mystica_recipes():
    recipe = Recipe(*["Rice"] * 6, *["Wasabi"] * 2, *["Curry Powder"] * 2)
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.FIRE, 2)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.GRASS, 2)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.WATER, 1)

    recipe = Recipe(
        *["Chorizo"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, "Pepper", "Curry Powder"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.NORMAL, 1)

    recipe = Recipe(
        *["Chorizo"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.BUG, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.NORMAL, 1)

    recipe = Recipe(
        *["Chorizo"] * 4, *["Wasabi"] * 2, "Rice", "Potato Salad", *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.BUG, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.FIRE, 1)

    recipe = Recipe(
        *["Fried Fillet"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.WATER, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.FLYING, 1)
    assert effects[2] == Effect.from_enums(Power.TEENSY, Type.NORMAL, 1)

    recipe = Recipe(
        *["Fried Fillet"] * 4, *["Wasabi"] * 2, *["Rice"] * 2, *["Curry Powder"] * 2
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.WATER, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.FLYING, 1)
    assert effects[2] == Effect.from_enums(Power.TEENSY, Type.NORMAL, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.RAID, Type.FIRE, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.FIGHTING, 1)
    assert effects[2] == Effect.from_enums(Power.HUMUNGO, Type.GRASS, 1)

    recipe = Recipe("Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Wasabi")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect.from_enums(Power.RAID, Type.FLYING, 2)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.FIGHTING, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.FLYING, 2)
    assert effects[2] == Effect.from_enums(Power.TEENSY, Type.FIGHTING, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.FIRE, 2)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.WATER, 2)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.GRASS, 1)

    recipe = Recipe(
        "Egg",
        "Egg",
        "Egg",
        "Jalapeño",
        "Jalapeño",
        "Potato Salad",
        "Whipped Cream",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.RAID, Type.FAIRY, 2)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.GRASS, 1)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.ROCK, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.RAID, Type.WATER, 2)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.GRASS, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.RAID, Type.GRASS, 2)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.WATER, 2)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.FIRE, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.PSYCHIC, 2)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.GHOST, 2)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.FIGHTING, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.RAID, Type.FLYING, 2)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.WATER, 2)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.FIRE, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.EXP_POINT, Type.FLYING, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.PSYCHIC, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.ELECTRIC, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.EXP_POINT, Type.FLYING, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.FIGHTING, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.NORMAL, 1)

    recipe = Recipe(
        "Hamburger", "Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Ketchup"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.POISON, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.POISON, 1)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.DRAGON, 1)

    recipe = Recipe(
        "Rice", "Rice", "Rice", "Rice", "Rice", "Rice", "Pepper", "Whipped Cream"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.HUMUNGO, Type.NORMAL, 2)
    assert effects[1] == Effect.from_enums(Power.RAID, Type.FIGHTING, 2)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.FLYING, 1)

    recipe = Recipe(
        "Egg",
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
    assert effects[0] == Effect.from_enums(Power.RAID, Type.ICE, 2)
    assert effects[1] == Effect.from_enums(Power.HUMUNGO, Type.ELECTRIC, 1)
    assert effects[2] == Effect.from_enums(Power.ENCOUNTER, Type.ROCK, 1)

    recipe = Recipe("Onion", "Onion", "Onion", "Onion", "Butter")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.RAID, Type.PSYCHIC, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.BUG, 1)

    recipe = Recipe("Onion", "Onion", "Onion", "Onion", "Strawberry", "Salt")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.RAID, Type.PSYCHIC, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.FIGHTING, 1)

    """recipe = Recipe(
        ["Hamburger"] * 5, "Red Bell Pepper", "Peanut Butter", "Peanut Butter"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.FIRE, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.NORMAL, 1)"""

    recipe = Recipe(
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Kiwi",
        "Kiwi",
        "Chili Sauce",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ITEM_DROP, Type.POISON, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.FIRE, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.BUG, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.FIRE, 1)


def test_split_types():

    recipe = Recipe(
        "Hamburger", "Hamburger", "Hamburger", "Hamburger", "Hamburger", "Butter"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.GHOST, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.STEEL, 1)

    recipe = Recipe(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.GHOST, 1)

    recipe = Recipe(
        "Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Watercress", "Salt"
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.FIGHTING, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.FLYING, 1)

    recipe = Recipe("Prosciutto", "Prosciutto", "Prosciutto", "Prosciutto", "Ketchup")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.FLYING, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.NORMAL, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.FLYING, 1)

    recipe = Recipe(
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Green Bell Pepper",
        "Ketchup",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ITEM_DROP, Type.POISON, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.NORMAL, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.POISON, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.TEENSY, Type.POISON, 1)
    assert effects[1] == Effect.from_enums(Power.ENCOUNTER, Type.DRAGON, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.POISON, 1)

    recipe = Recipe(
        "Cheese",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.GHOST, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)

    recipe = Recipe("Ham", "Ham", "Ham", "Ham", "Mustard")
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.GROUND, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.NORMAL, 1)
    assert effects[2] == Effect.from_enums(Power.EXP_POINT, Type.GROUND, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.RAID, Type.NORMAL, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.STEEL, 1)

    recipe = Recipe(
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
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.CATCHING, Type.STEEL, 1)
    assert effects[2] == Effect.from_enums(Power.RAID, Type.NORMAL, 1)

    recipe = Recipe(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Peanut Butter",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.NORMAL, 1)

    recipe = Recipe(
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Hamburger",
        "Mustard",
    )
    effects = recipe.effects
    assert effects[0] == Effect.from_enums(Power.ENCOUNTER, Type.STEEL, 1)
    assert effects[1] == Effect.from_enums(Power.EXP_POINT, Type.STEEL, 1)
    assert effects[2] == Effect.from_enums(Power.CATCHING, Type.ROCK, 1)
