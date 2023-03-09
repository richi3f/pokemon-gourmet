from enum import Enum, auto


class _ReprEnum(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class Flavor(_ReprEnum):
    SWEET = auto()
    SALTY = auto()
    SOUR = auto()
    BITTER = auto()
    HOT = auto()


class Power(_ReprEnum):
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
    NONE = 0
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
