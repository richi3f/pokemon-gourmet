__all__ = ["InvalidEffects", "RepeatedPowers", "UnexpectedPower", "UnexpectedType"]


class InvalidEffects(ValueError):
    """Invalid combination of effects in a list of desired effects."""

    ...


class RepeatedPowers(ValueError):
    """Two or more Powers of the same type repeated in a list of desired
    effects."""

    ...


class UnexpectedPower(KeyError):
    """Power not found."""

    ...


class UnexpectedType(KeyError):
    """Pokémon Type not found."""

    ...
