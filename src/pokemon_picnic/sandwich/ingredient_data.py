__all__ = ["CONDIMENTS", "FILLINGS", "get_ingredient"]

from pokemon_picnic.core.enums import Flavor, Power, Type
from pokemon_picnic.sandwich.ingredient import Condiment, Filling

CONDIMENTS = [
    Condiment(
        name="Mayonnaise",
        flavor={Flavor.SALTY: 8, Flavor.SOUR: 20},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.NORMAL: 2, Type.FIGHTING: 2},
    ),
    Condiment(
        name="Ketchup",
        flavor={Flavor.SWEET: 8, Flavor.SALTY: 16, Flavor.SOUR: 16},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.FLYING: 2, Type.POISON: 2},
    ),
    Condiment(
        name="Mustard",
        flavor={
            Flavor.SWEET: 4,
            Flavor.SALTY: 8,
            Flavor.SOUR: 8,
            Flavor.BITTER: 8,
            Flavor.HOT: 16,
        },
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.GROUND: 2, Type.ROCK: 2},
    ),
    Condiment(
        name="Butter",
        flavor={Flavor.SWEET: 12, Flavor.SALTY: 12},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.BUG: 2, Type.GHOST: 2},
    ),
    Condiment(
        name="Peanut Butter",
        flavor={Flavor.SWEET: 16, Flavor.SALTY: 12},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.STEEL: 2, Type.FIRE: 2},
    ),
    Condiment(
        name="Chili Sauce",
        flavor={Flavor.SWEET: 8, Flavor.SALTY: 12, Flavor.SOUR: 8, Flavor.HOT: 20},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.WATER: 2, Type.GRASS: 2},
    ),
    Condiment(
        name="Salt",
        flavor={Flavor.SALTY: 20, Flavor.BITTER: 4},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.ELECTRIC: 2, Type.PSYCHIC: 2},
    ),
    Condiment(
        name="Pepper",
        flavor={Flavor.SALTY: 4, Flavor.BITTER: 8, Flavor.HOT: 16},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.ICE: 2, Type.DRAGON: 2},
    ),
    Condiment(
        name="Yogurt",
        flavor={Flavor.SWEET: 16, Flavor.SOUR: 16},
        power={Power.EGG: -3, Power.EXP_POINT: 12, Power.RAID: 21},
        pokemon_type={Type.DARK: 2, Type.FAIRY: 2},
    ),
    Condiment(
        name="Whipped Cream",
        flavor={Flavor.SWEET: 20},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.NORMAL: 4, Type.FLYING: 4, Type.GROUND: 4},
    ),
    Condiment(
        name="Cream Cheese",
        flavor={Flavor.SWEET: 12, Flavor.SALTY: 12, Flavor.SOUR: 12},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.BUG: 4, Type.STEEL: 4, Type.WATER: 4},
    ),
    Condiment(
        name="Jam",
        flavor={Flavor.SWEET: 16, Flavor.SALTY: 4, Flavor.SOUR: 16},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.ELECTRIC: 4, Type.ICE: 4, Type.DARK: 4},
    ),
    Condiment(
        name="Marmalade",
        flavor={Flavor.SWEET: 12, Flavor.SALTY: 4, Flavor.SOUR: 16, Flavor.BITTER: 20},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.FIGHTING: 4, Type.POISON: 4, Type.ROCK: 4},
    ),
    Condiment(
        name="Olive Oil",
        flavor={Flavor.SOUR: 4, Flavor.BITTER: 4},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.GHOST: 4, Type.FIRE: 4, Type.GRASS: 4},
    ),
    Condiment(
        name="Vinegar",
        flavor={Flavor.SWEET: 4, Flavor.SOUR: 20, Flavor.BITTER: 4},
        power={
            Power.EGG: 5,
            Power.EXP_POINT: -3,
            Power.ITEM_DROP: 12,
            Power.TEENSY: -15,
        },
        pokemon_type={Type.PSYCHIC: 4, Type.DRAGON: 4, Type.FAIRY: 4},
    ),
    Condiment(
        name="Horseradish",
        flavor={Flavor.SWEET: 4, Flavor.HOT: 16},
        power={Power.HUMUNGO: -3, Power.TEENSY: 21, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.NORMAL: 2,
            Type.FIGHTING: 2,
            Type.FLYING: 2,
            Type.POISON: 2,
            Type.GROUND: 2,
            Type.ROCK: 2,
        },
    ),
    Condiment(
        name="Curry Powder",
        flavor={
            Flavor.SWEET: 4,
            Flavor.SALTY: 4,
            Flavor.SOUR: 4,
            Flavor.BITTER: 12,
            Flavor.HOT: 30,
        },
        power={Power.HUMUNGO: -3, Power.TEENSY: 21, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.BUG: 2,
            Type.GHOST: 2,
            Type.STEEL: 2,
            Type.FIRE: 2,
            Type.WATER: 2,
            Type.GRASS: 2,
        },
    ),
    Condiment(
        name="Wasabi",
        flavor={Flavor.SWEET: 4, Flavor.SALTY: 4, Flavor.HOT: 20},
        power={Power.HUMUNGO: -3, Power.TEENSY: 21, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.ELECTRIC: 2,
            Type.PSYCHIC: 2,
            Type.ICE: 2,
            Type.DRAGON: 2,
            Type.DARK: 2,
            Type.FAIRY: 2,
        },
    ),
    Condiment(
        name="Sweet Herba Mystica",
        flavor={Flavor.SWEET: 500},
        power={Power.TITLE: 1000, Power.SPARKLING: 1000},
        pokemon_type={
            Type.NORMAL: 250,
            Type.FIGHTING: 250,
            Type.FLYING: 250,
            Type.POISON: 250,
            Type.GROUND: 250,
            Type.ROCK: 250,
            Type.BUG: 250,
            Type.GHOST: 250,
            Type.STEEL: 250,
            Type.FIRE: 250,
            Type.WATER: 250,
            Type.GRASS: 250,
            Type.ELECTRIC: 250,
            Type.PSYCHIC: 250,
            Type.ICE: 250,
            Type.DRAGON: 250,
            Type.DARK: 250,
            Type.FAIRY: 250,
        },
    ),
    Condiment(
        name="Salty Herba Mystica",
        flavor={Flavor.SALTY: 500},
        power={Power.TITLE: 1000, Power.SPARKLING: 1000},
        pokemon_type={
            Type.NORMAL: 250,
            Type.FIGHTING: 250,
            Type.FLYING: 250,
            Type.POISON: 250,
            Type.GROUND: 250,
            Type.ROCK: 250,
            Type.BUG: 250,
            Type.GHOST: 250,
            Type.STEEL: 250,
            Type.FIRE: 250,
            Type.WATER: 250,
            Type.GRASS: 250,
            Type.ELECTRIC: 250,
            Type.PSYCHIC: 250,
            Type.ICE: 250,
            Type.DRAGON: 250,
            Type.DARK: 250,
            Type.FAIRY: 250,
        },
    ),
    Condiment(
        name="Sour Herba Mystica",
        flavor={Flavor.SOUR: 500},
        power={Power.TITLE: 1000, Power.SPARKLING: 1000},
        pokemon_type={
            Type.NORMAL: 250,
            Type.FIGHTING: 250,
            Type.FLYING: 250,
            Type.POISON: 250,
            Type.GROUND: 250,
            Type.ROCK: 250,
            Type.BUG: 250,
            Type.GHOST: 250,
            Type.STEEL: 250,
            Type.FIRE: 250,
            Type.WATER: 250,
            Type.GRASS: 250,
            Type.ELECTRIC: 250,
            Type.PSYCHIC: 250,
            Type.ICE: 250,
            Type.DRAGON: 250,
            Type.DARK: 250,
            Type.FAIRY: 250,
        },
    ),
    Condiment(
        name="Bitter Herba Mystica",
        flavor={Flavor.BITTER: 500},
        power={Power.TITLE: 1000, Power.SPARKLING: 1000},
        pokemon_type={
            Type.NORMAL: 250,
            Type.FIGHTING: 250,
            Type.FLYING: 250,
            Type.POISON: 250,
            Type.GROUND: 250,
            Type.ROCK: 250,
            Type.BUG: 250,
            Type.GHOST: 250,
            Type.STEEL: 250,
            Type.FIRE: 250,
            Type.WATER: 250,
            Type.GRASS: 250,
            Type.ELECTRIC: 250,
            Type.PSYCHIC: 250,
            Type.ICE: 250,
            Type.DRAGON: 250,
            Type.DARK: 250,
            Type.FAIRY: 250,
        },
    ),
    Condiment(
        name="Spicy Herba Mystica",
        flavor={Flavor.HOT: 500},
        power={Power.TITLE: 1000, Power.SPARKLING: 1000},
        pokemon_type={
            Type.NORMAL: 250,
            Type.FIGHTING: 250,
            Type.FLYING: 250,
            Type.POISON: 250,
            Type.GROUND: 250,
            Type.ROCK: 250,
            Type.BUG: 250,
            Type.GHOST: 250,
            Type.STEEL: 250,
            Type.FIRE: 250,
            Type.WATER: 250,
            Type.GRASS: 250,
            Type.ELECTRIC: 250,
            Type.PSYCHIC: 250,
            Type.ICE: 250,
            Type.DRAGON: 250,
            Type.DARK: 250,
            Type.FAIRY: 250,
        },
    ),
]

FILLINGS = [
    Filling(
        name="Lettuce",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.BITTER: 2},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.GRASS: 6},
    ),
    Filling(
        name="Tomato",
        pieces=3,
        flavor={Flavor.SWEET: 2, Flavor.SOUR: 4, Flavor.BITTER: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.FAIRY: 6},
    ),
    Filling(
        name="Cherry Tomatoes",
        pieces=3,
        flavor={Flavor.SWEET: 3, Flavor.SOUR: 5, Flavor.BITTER: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.BUG: 6},
    ),
    Filling(
        name="Cucumber",
        pieces=3,
        flavor={Flavor.SOUR: 1, Flavor.BITTER: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.WATER: 6},
    ),
    Filling(
        name="Pickle",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SOUR: 4, Flavor.BITTER: 2},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.FIGHTING: 6},
    ),
    Filling(
        name="Onion",
        pieces=3,
        flavor={Flavor.SWEET: 2, Flavor.BITTER: 1, Flavor.HOT: 3},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.PSYCHIC: 6},
    ),
    Filling(
        name="Red Onion",
        pieces=3,
        flavor={Flavor.SWEET: 3, Flavor.BITTER: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.GHOST: 6},
    ),
    Filling(
        name="Green Bell Pepper",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SOUR: 1, Flavor.BITTER: 5},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.POISON: 6},
    ),
    Filling(
        name="Red Bell Pepper",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SOUR: 1, Flavor.BITTER: 3},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.FIRE: 6},
    ),
    Filling(
        name="Yellow Bell Pepper",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SOUR: 1, Flavor.BITTER: 3},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.ELECTRIC: 6},
    ),
    Filling(
        name="Avocado",
        pieces=3,
        flavor={Flavor.SWEET: 3, Flavor.SOUR: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.DRAGON: 6},
    ),
    Filling(
        name="Bacon",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 5, Flavor.SOUR: 1, Flavor.BITTER: 4},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.ROCK: 6},
    ),
    Filling(
        name="Ham",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 5},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.GROUND: 6},
    ),
    Filling(
        name="Prosciutto",
        pieces=3,
        flavor={Flavor.SWEET: 2, Flavor.SALTY: 4, Flavor.SOUR: 1},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.FLYING: 6},
    ),
    Filling(
        name="Chorizo",
        pieces=3,
        flavor={Flavor.SALTY: 4, Flavor.BITTER: 2, Flavor.HOT: 4},
        power={Power.EXP_POINT: 7, Power.ITEM_DROP: -1, Power.ENCOUNTER: 4},
        pokemon_type={
            Type.NORMAL: 12,
            Type.POISON: 12,
            Type.BUG: 12,
            Type.FIRE: 12,
            Type.ELECTRIC: 12,
            Type.DRAGON: 12,
        },
    ),
    Filling(
        name="Herbed Sausage",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 4, Flavor.BITTER: 4},
        power={Power.EXP_POINT: 7, Power.ITEM_DROP: -1, Power.ENCOUNTER: 4},
        pokemon_type={
            Type.FIGHTING: 12,
            Type.GROUND: 12,
            Type.GHOST: 12,
            Type.WATER: 12,
            Type.PSYCHIC: 12,
            Type.DARK: 12,
        },
    ),
    Filling(
        name="Hamburger",
        pieces=1,
        flavor={Flavor.SWEET: 6, Flavor.SALTY: 12, Flavor.BITTER: 9},
        power={Power.CATCHING: 12, Power.RAID: -3, Power.ENCOUNTER: 21},
        pokemon_type={Type.STEEL: 18},
    ),
    Filling(
        name="Klawf Stick",
        pieces=3,
        flavor={Flavor.SWEET: 4, Flavor.SALTY: 4},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.ICE: 6},
    ),
    Filling(
        name="Smoked Fillet",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 3, Flavor.SOUR: 2, Flavor.BITTER: 3},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.DARK: 6},
    ),
    Filling(
        name="Fried Fillet",
        pieces=1,
        flavor={Flavor.SWEET: 2, Flavor.SALTY: 3, Flavor.BITTER: 3},
        power={Power.CATCHING: 21, Power.RAID: 12, Power.ENCOUNTER: -3},
        pokemon_type={
            Type.NORMAL: 20,
            Type.FLYING: 20,
            Type.GROUND: 20,
            Type.BUG: 20,
            Type.STEEL: 20,
            Type.WATER: 20,
            Type.ELECTRIC: 20,
            Type.ICE: 20,
            Type.DARK: 20,
        },
    ),
    Filling(
        name="Sliced Egg",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 2, Flavor.BITTER: 1},
        power={Power.EXP_POINT: 7, Power.ITEM_DROP: -1, Power.ENCOUNTER: 4},
        pokemon_type={
            Type.FLYING: 12,
            Type.ROCK: 12,
            Type.STEEL: 12,
            Type.GRASS: 12,
            Type.ICE: 12,
            Type.FAIRY: 12,
        },
    ),
    Filling(
        name="Potato Tortilla",
        pieces=1,
        flavor={
            Flavor.SWEET: 3,
            Flavor.SALTY: 4,
            Flavor.SOUR: 1,
            Flavor.BITTER: 3,
            Flavor.HOT: 1,
        },
        power={Power.CATCHING: 21, Power.RAID: 12, Power.ENCOUNTER: -3},
        pokemon_type={
            Type.FIGHTING: 20,
            Type.POISON: 20,
            Type.ROCK: 20,
            Type.GHOST: 20,
            Type.FIRE: 20,
            Type.GRASS: 20,
            Type.PSYCHIC: 20,
            Type.DRAGON: 20,
            Type.FAIRY: 20,
        },
    ),
    Filling(
        name="Tofu",
        pieces=3,
        flavor={Flavor.SWEET: 3},
        power={Power.CATCHING: 4, Power.RAID: -1, Power.ENCOUNTER: 7},
        pokemon_type={Type.NORMAL: 6},
    ),
    Filling(
        name="Rice",
        pieces=1,
        flavor={Flavor.SWEET: 3, Flavor.SOUR: 1},
        power={Power.HUMUNGO: 21, Power.TEENSY: -3, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.NORMAL: 30,
            Type.FIGHTING: 30,
            Type.FLYING: 30,
            Type.FIRE: 30,
            Type.WATER: 30,
            Type.GRASS: 30,
        },
    ),
    Filling(
        name="Noodles",
        pieces=1,
        flavor={Flavor.SALTY: 4},
        power={Power.HUMUNGO: 21, Power.TEENSY: -3, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.POISON: 30,
            Type.GROUND: 30,
            Type.ROCK: 30,
            Type.ELECTRIC: 30,
            Type.PSYCHIC: 30,
            Type.ICE: 30,
        },
    ),
    Filling(
        name="Potato Salad",
        pieces=1,
        flavor={Flavor.SWEET: 2, Flavor.SALTY: 3, Flavor.SOUR: 4, Flavor.BITTER: 1},
        power={Power.HUMUNGO: 21, Power.TEENSY: -3, Power.ENCOUNTER: 12},
        pokemon_type={
            Type.BUG: 30,
            Type.GHOST: 30,
            Type.STEEL: 30,
            Type.DRAGON: 30,
            Type.DARK: 30,
            Type.FAIRY: 30,
        },
    ),
    Filling(
        name="Cheese",
        pieces=3,
        flavor={Flavor.SWEET: 1, Flavor.SALTY: 3},
        power={
            Power.CATCHING: 2,
            Power.EXP_POINT: 2,
            Power.ITEM_DROP: 2,
            Power.ENCOUNTER: -2,
        },
        pokemon_type={
            Type.NORMAL: 5,
            Type.FIGHTING: 5,
            Type.FLYING: 5,
            Type.POISON: 5,
            Type.GROUND: 5,
            Type.ROCK: 5,
            Type.BUG: 5,
            Type.GHOST: 5,
            Type.STEEL: 5,
            Type.FIRE: 5,
            Type.WATER: 5,
            Type.GRASS: 5,
            Type.ELECTRIC: 5,
            Type.PSYCHIC: 5,
            Type.ICE: 5,
            Type.DRAGON: 5,
            Type.DARK: 5,
            Type.FAIRY: 5,
        },
    ),
    Filling(
        name="Banana",
        pieces=3,
        flavor={Flavor.SWEET: 4, Flavor.SOUR: 1},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.NORMAL: 7, Type.BUG: 7, Type.ELECTRIC: 7},
    ),
    Filling(
        name="Strawberry",
        pieces=3,
        flavor={Flavor.SWEET: 4, Flavor.SOUR: 4},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.FIGHTING: 7, Type.GHOST: 7, Type.PSYCHIC: 7},
    ),
    Filling(
        name="Apple",
        pieces=3,
        flavor={Flavor.SWEET: 4, Flavor.SOUR: 3, Flavor.BITTER: 1},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.FLYING: 7, Type.STEEL: 7, Type.ICE: 7},
    ),
    Filling(
        name="Kiwi",
        pieces=3,
        flavor={Flavor.SWEET: 2, Flavor.SOUR: 5, Flavor.BITTER: 1},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.POISON: 7, Type.FIRE: 7, Type.DRAGON: 7},
    ),
    Filling(
        name="Pineapple",
        pieces=3,
        flavor={Flavor.SWEET: 3, Flavor.SOUR: 5, Flavor.BITTER: 1},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.GROUND: 7, Type.WATER: 7, Type.DARK: 7},
    ),
    Filling(
        name="Jalapeno",
        pieces=3,
        flavor={Flavor.SOUR: 2, Flavor.HOT: 5},
        power={Power.EGG: 4, Power.CATCHING: -1, Power.ITEM_DROP: 7, Power.HUMUNGO: -5},
        pokemon_type={Type.ROCK: 7, Type.GRASS: 7, Type.FAIRY: 7},
    ),
    Filling(
        name="Watercress",
        pieces=3,
        flavor={Flavor.SALTY: 1, Flavor.SOUR: 2, Flavor.BITTER: 5, Flavor.HOT: 1},
        power={Power.EGG: 2, Power.RAID: 2, Power.ENCOUNTER: -2},
        pokemon_type={
            Type.NORMAL: 1,
            Type.FIGHTING: 1,
            Type.FLYING: 1,
            Type.POISON: 1,
            Type.GROUND: 1,
            Type.ROCK: 1,
            Type.BUG: 1,
            Type.GHOST: 1,
            Type.STEEL: 1,
        },
    ),
    Filling(
        name="Basil",
        pieces=4,
        flavor={Flavor.SALTY: 1, Flavor.SOUR: 1, Flavor.BITTER: 4},
        power={Power.EGG: 2, Power.RAID: 2, Power.ENCOUNTER: -2},
        pokemon_type={
            Type.FIRE: 1,
            Type.WATER: 1,
            Type.GRASS: 1,
            Type.ELECTRIC: 1,
            Type.PSYCHIC: 1,
            Type.ICE: 1,
            Type.DRAGON: 1,
            Type.DARK: 1,
            Type.FAIRY: 1,
        },
    ),
]


def get_ingredient(name: str):
    for ingredient in CONDIMENTS + FILLINGS:
        if ingredient.name == name:
            return ingredient
    raise KeyError(f"Ingredient data not found: {name}")
