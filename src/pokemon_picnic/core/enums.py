from enum import Enum, auto


class Flavor(Enum):
    SWEET = auto()
    SPICY = auto()
    SOUR = auto()
    BITTER = auto()
    HOT = auto()


class Power(Enum):
    EGG = "Egg Power"
    CATCHING = "Catching Power"
    ITEM = "Item Drop Power"
    HUMUNGO = "Humungo Power"
    TEENSY = "Teensy Power"
    RAID = "Raid Power"
    ENCOUNTER = "Encounter Power"
    EXP_POINT = "Exp. Point Power"
    TITLE = "Title Power"
    SPARKLING = "Sparkling Power"


class Type(Enum):
    NORMAL = auto()
    FIGHTING = auto()
    FLYING = auto()
    POISON = auto()
    GROUND = auto()
    ROCK = auto()
    BUG = auto()
    GHOST = auto()
    STEEL = auto()
    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    ELECTRIC = auto()
    PSYCHIC = auto()
    ICE = auto()
    DRAGON = auto()
    DARK = auto()
    FAIRY = auto()
