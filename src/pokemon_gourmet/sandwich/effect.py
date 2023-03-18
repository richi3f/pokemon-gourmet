__all__ = ["Effect", "EffectList"]

from dataclasses import astuple, dataclass
from typing import AbstractSet, Iterable, Iterator, Optional, Union, cast

from pokemon_gourmet.enums import Power, Type

EffectLevel = Optional[int]
EffectType = Optional[Type]
EffectTuple = tuple[Power, EffectType, EffectLevel]


@dataclass(unsafe_hash=True)
class Effect:
    power: Power
    pokemon_type: EffectType
    level: EffectLevel = None

    def __iter__(self) -> Iterator[Union[Power, Type, int, None]]:
        return iter(astuple(self))

    def __repr__(self) -> str:
        repr_ = f"{self.power.name} Power"
        if self.pokemon_type is not None:
            repr_ += f": {self.pokemon_type.name}"
        if self.level is not None:
            repr_ += f" Lv. {self.level}"
        return repr_


class EffectList(AbstractSet):
    def __init__(self, effects: Iterable[Union[Effect, EffectTuple]]) -> None:
        self.powers: set[Power] = set()
        self.types: set[EffectType] = set()
        self.tuples: list[Effect] = []
        for tup in effects:
            effect = Effect(*cast(EffectTuple, tup))
            if effect not in self.tuples:
                self.powers.add(effect.power)
                self.types.add(effect.pokemon_type)
                self.tuples.append(effect)

    def __contains__(self, value: Union[Power, Type, Effect, tuple]) -> bool:
        if isinstance(value, (Effect, tuple)):
            if isinstance(value, tuple):
                value = Effect(*value)
            return value in self.tuples
        return value in self.powers.union(self.types)

    def __getitem__(self, index: int) -> Effect:
        return self.tuples[index]

    def __iter__(self) -> Iterator[Effect]:
        return iter(self.tuples)

    def __len__(self) -> int:
        return len(self.tuples)

    def __repr__(self) -> str:
        return ",\n".join(map(str, self.tuples))

    def remove_levels(self) -> list[int]:
        """Remove and return effect levels."""
        levels = []
        for i in range(len(self)):
            levels.append(self.tuples[i].level)
            self.tuples[i].level = None
        return levels
