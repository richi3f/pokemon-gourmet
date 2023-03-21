__all__ = ["Flavor", "Power", "Type"]

from enum import Enum, auto


class _ReprEnum(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class Flavor(_ReprEnum):
    """Flavor of an ingredient or a sandwich"""

    SWEET = auto()
    SALTY = auto()
    SOUR = auto()
    BITTER = auto()
    HOT = auto()


class Power(_ReprEnum):
    """Power of an ingredient, a sandwich, or an effect"""

    EGG = auto()
    CATCHING = auto()
    EXP_POINT = auto()
    ITEM_DROP = auto()
    RAID = auto()
    SPARKLING = auto()
    TITLE = auto()
    HUMUNGO = auto()
    TEENSY = auto()
    ENCOUNTER = auto()


class Type(_ReprEnum):
    """A Pokémon Type associated to an ingredient, a sandwich, or an effect"""

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
