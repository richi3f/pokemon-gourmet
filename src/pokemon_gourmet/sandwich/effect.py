__all__ = ["Effect", "EffectList"]

from dataclasses import astuple, dataclass
from typing import AbstractSet, Iterable, Iterator, Optional, Union, cast

import numpy as np
from numpy.typing import NDArray

from pokemon_gourmet.enums import Power, Type

EffectLevel = Optional[int]
EffectType = Optional[Type]
EffectTypeIndex = Optional[int]
IncompleteEffectTuple = tuple[Power, EffectType]
CompelteEffectTuple = tuple[Power, EffectType, EffectLevel]
EffectTuple = Union[IncompleteEffectTuple, CompelteEffectTuple]


@dataclass(unsafe_hash=True)
class Effect:
    """A tuple of Power, Type, and level"""

    power_idx: int
    pokemon_type_idx: EffectTypeIndex
    level: EffectLevel = None

    @property
    def power(self) -> Power:
        return Power(self.power_idx + 1)

    @property
    def pokemon_type(self) -> Optional[Type]:
        if self.pokemon_type_idx is None:
            return None
        return Type(self.pokemon_type_idx + 1)

    def __iter__(self) -> Iterator[Union[Power, Type, int, None]]:
        return iter(astuple(self))

    def __repr__(self) -> str:
        repr_ = f"{self.power}"
        if self.pokemon_type is not None:
            repr_ += f": {self.pokemon_type}"
        if self.level is not None:
            repr_ += f" Lv. {self.level}"
        return repr_

    @classmethod
    def from_enums(
        cls, power: Power, pokemon_type: Optional[Type], level: EffectLevel = None
    ):
        type_ = None if pokemon_type is None else pokemon_type.value - 1
        return cls(power.value - 1, type_, level)


class EffectList(AbstractSet):
    """A list of unique effect tuples, that supports set operations"""

    def __init__(self, effects: Union[NDArray[np.intp], Iterable[EffectTuple]]) -> None:
        self.powers: set[int] = set()
        self.types: set[EffectTypeIndex] = set()
        self.tuples: list[Effect] = []
        for row in effects:
            if isinstance(row, tuple):
                effect = Effect.from_enums(*cast(CompelteEffectTuple, row))
            else:
                effect = Effect(*row)
            if effect not in self.tuples:
                self.powers.add(effect.power_idx)
                self.types.add(effect.pokemon_type_idx)
                self.tuples.append(effect)

    def __contains__(self, value: Union[Power, Type, Effect, tuple]) -> bool:
        if isinstance(value, (Effect, tuple)):
            if isinstance(value, tuple):
                value = Effect.from_enums(*value)
            return value in self.tuples
        if isinstance(value, Power):
            return (value.value - 1) in self.powers
        return (value.value - 1) in self.types

    def __getitem__(self, index: int) -> Effect:
        return self.tuples[index]

    def __iter__(self) -> Iterator[Effect]:
        return iter(self.tuples)

    def __len__(self) -> int:
        return len(self.tuples)

    def __repr__(self) -> str:
        return ",\n".join(map(str, self.tuples))

    def index(self, value: int) -> int:
        for i, effect in enumerate(self.tuples):
            if effect.power_idx == value:
                return i
        raise ValueError()

    def remove_levels(self) -> list[int]:
        """Remove and return effect levels."""
        levels = []
        for i in range(len(self)):
            levels.append(self.tuples[i].level)
            self.tuples[i].level = None
        return levels
