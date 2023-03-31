from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich import Effect, EffectList


def test_membership():
    effect_tuples = [
        (Power.RAID, Type.GRASS, 1),
        (Power.EXP_POINT, Type.FIRE, 2),
        (Power.HUMUNGO, Type.WATER, 3),
    ]
    powers, types, _ = zip(*effect_tuples)
    effects = EffectList(effect_tuples)
    # Check power/type in effect list
    assert all(power in effects for power in powers)
    assert all(type_ in effects for type_ in types)
    assert all(
        power not in effects
        for power in Power.__members__.values()
        if power not in powers
    )
    assert all(
        type_ not in effects
        for type_ in Type.__members__.values()
        if type_ not in types
    )
    # Check power/type/level tuple in effect list
    assert all(tup in effects for tup in effect_tuples)
    assert (Power.RAID, Type.GRASS, 2) not in effects
    assert all(Effect.from_enums(*tup) in effects for tup in effect_tuples)
    assert Effect.from_enums(Power.RAID, Type.GRASS, 2) not in effects


def test_remove_levels():
    effects = EffectList(
        [
            (Power.SPARKLING, Type.DRAGON, 1),
            (Power.TITLE, Type.FAIRY, 2),
            (Power.TEENSY, Type.BUG, 3),
        ]
    )
    levels = effects.remove_levels()
    assert levels == [1, 2, 3]
    assert all(effect.level is None for effect in effects.tuples)


def test_intersection():
    a_list = EffectList(
        [(Power.EGG, None), (Power.ENCOUNTER, Type.FAIRY), (Power.CATCHING, Type.BUG)]
    )
    b_list = EffectList(
        [
            (Power.ENCOUNTER, Type.GRASS),
            (Power.CATCHING, Type.BUG),
            (Power.RAID, Type.WATER),
        ]
    )
    assert len(a_list & b_list) == 1

    c_list = EffectList(
        [
            (Power.ITEM_DROP, Type.GHOST),
            (Power.ENCOUNTER, Type.FAIRY, 1),
            (Power.CATCHING, Type.BUG, 3),
        ]
    )
    assert len(a_list & c_list) == 0

    c_list.remove_levels()
    assert len(a_list & c_list) == 2
