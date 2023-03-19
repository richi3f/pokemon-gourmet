__all__ = ["InvalidEffects", "UnexpectedPower", "UnexpectedType"]


class InvalidEffects(ValueError):
    """Invalid combination of effects in a list of desired effects."""

    ...


class UnexpectedPower(KeyError):
    """Power not found."""

    ...


class UnexpectedType(KeyError):
    """Pokémon Type not found."""

    ...
