__all__ = ["InvalidEffects", "RepeatedPowers", "TypedEggPower", "UnexpectedPower", "UnexpectedType"]


class InvalidEffects(ValueError):
    """Invalid combination of effects in a list of desired effects."""

    ...


class RepeatedPowers(ValueError):
    """Two or more Powers of the same type repeated in a list of desired
    effects."""

    ...


class TypedEggPower(ValueError):
    """Egg Power should be typeless."""

    ...


class UnexpectedPower(KeyError):
    """Power not found."""

    ...


class UnexpectedType(KeyError):
    """Pokémon Type not found."""

    ...
