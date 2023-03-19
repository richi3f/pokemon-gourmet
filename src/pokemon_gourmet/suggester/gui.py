__all__ = []

import inspect
from functools import partial
from math import sqrt
from numbers import Number
from pathlib import Path
from typing import Optional, cast

import pandas as pd
import streamlit as st
from griffe.dataclasses import Docstring
from griffe.docstrings.dataclasses import DocstringSectionParameters
from griffe.docstrings.parsers import Parser

from pokemon_gourmet.enums import Power, Type
from pokemon_gourmet.sandwich.effect import Effect, EffectList
from pokemon_gourmet.sandwich.ingredient import Condiment, Filling, Ingredient
from pokemon_gourmet.suggester import exceptions as e
from pokemon_gourmet.suggester.generator import RecipeGenerator
from pokemon_gourmet.suggester.mcts import policies as p
from pokemon_gourmet.suggester.mcts.state import Sandwich

POWERS = [""] + Power._member_names_
TYPES = [""] + Type._member_names_
TYPE_COLORS = {
    Type.NORMAL: (159, 161, 159),
    Type.FIGHTING: (255, 128, 0),
    Type.FLYING: (129, 185, 239),
    Type.POISON: (145, 65, 203),
    Type.GROUND: (190, 151, 122),
    Type.ROCK: (175, 169, 129),
    Type.BUG: (121, 138, 10),
    Type.GHOST: (112, 65, 112),
    Type.STEEL: (96, 161, 184),
    Type.FIRE: (230, 40, 41),
    Type.WATER: (41, 128, 239),
    Type.GRASS: (64, 161, 41),
    Type.ELECTRIC: (250, 192, 0),
    Type.PSYCHIC: (239, 65, 121),
    Type.ICE: (63, 216, 255),
    Type.DRAGON: (80, 96, 225),
    Type.DARK: (80, 65, 63),
    Type.FAIRY: (240, 118, 220),
}


def get_target_attr(attr_name: str) -> list[str]:
    """Return a list of attribute values from the session state."""
    return [st.session_state[f"{attr_name}{i}"] for i in range(3)]


def update_target_selectboxes() -> None:
    """Update the target Power and Type selectboxes. If Egg Power is selected,
    its corresponding Type selectbox is blanked and disabled. If Sparkling
    Power is selected, all Type selectboxes are disabled and forced to match
    the Sparkling Power's Type."""
    power_names = get_target_attr("power")
    type_names = get_target_attr("type")
    try:
        sparkling_idx = power_names.index(Power.SPARKLING.name)
    except ValueError:
        sparkling_idx = -1
    for i, power_name in enumerate(power_names):
        # Disable if Egg power
        is_egg = power_name == Power.EGG.name
        st.session_state.disabled_type[i] = is_egg
        if is_egg:
            st.session_state[f"type{i}"] = ""
        elif sparkling_idx >= 0:
            # Sparkling power forces all types to be same
            if i != sparkling_idx:
                st.session_state.disabled_type[i] = True
                st.session_state[f"type{i}"] = type_names[sparkling_idx]


def slugify_rollout_policy_name(func_name: Optional[str]) -> str:
    return str(func_name).lower().replace(" ", "_")


def change_rollout_policy_desc() -> None:
    """Change the caption describing what each rollout policy does."""
    key = slugify_rollout_policy_name(st.session_state.rollout_policy)
    doc = p.ROLLOUT_POLICIES[key].__doc__
    if doc is not None:
        doc_section, *_ = Docstring(doc, parser=Parser.google).parsed
        st.session_state.rollout_policy_desc = getattr(doc_section, "value")


def get_rollout_policy_func(func_name: Optional[str]) -> p.RolloutPolicy:
    """Return a rollout policy function that takes one single argument (the
    current state). If the given function name takes more than one argument,
    create input boxes so users can change the values of the other arguments
    and return a partial function."""
    func_name = slugify_rollout_policy_name(func_name)
    if func_name not in p.ROLLOUT_POLICIES:
        raise ValueError("Unexpected rollout policy function name.")
    func = p.ROLLOUT_POLICIES[func_name]
    params = inspect.signature(func).parameters
    if len(params) > 1:
        # a rollout policy that takes additional parameters
        func_doc = func.__doc__
        if func_doc is not None:
            func_doc = Docstring(func_doc, parser=Parser.google)
            param_docs = []
            for section in func_doc.parsed:
                if isinstance(section, DocstringSectionParameters):
                    param_docs = section.value
        else:
            param_docs = None
        rollout_policy_kwargs = {}
        for i, param in enumerate(params.values()):
            if param.name == "state":
                continue
            if issubclass(param.annotation, Number):
                if param_docs:
                    label, desc = param_docs[i].description.split(". ", 1)
                else:
                    label, desc = param.name, None
                rollout_policy_kwargs[param.name] = st.number_input(
                    label, value=param.default, help=desc
                )
            else:
                raise ValueError("Unsupported parameter type.")
        func = partial(func, **rollout_policy_kwargs)
    return func


def parse_targets() -> EffectList:
    """Return a list of targets parsed from the session state. Run tests to
    validate the targets."""
    targets = []
    for i in range(3):
        power_str = st.session_state[f"power{i}"]
        if not power_str:
            raise e.UnexpectedPower(
                "Unexpected Power. Make sure to fill out every Power field."
            )
        power = Power[power_str]
        type_str = st.session_state[f"type{i}"]
        if not type_str:
            type_ = None
            if power != Power.EGG:
                raise e.UnexpectedType(
                    "Unexpected Type. Make sure to fill out every Type field."
                )
        else:
            type_ = Type[type_str]
        targets.append((power, type_))
    return EffectList(targets)


def get_effect_tag(effect: Effect) -> str:
    """Return an effect represented as HTML."""
    color = (
        TYPE_COLORS[effect.pokemon_type]
        if effect.pokemon_type is not None
        else (177, 211, 177)
    )
    return (
        "<span style='padding: 1px 6px; margin: 0 5px; display: inline-block; "
        "vertical-align: middle; border-radius: 3px; font-size: 0.75rem; "
        f"font-weight: 400; white-space: nowrap; border: 1px solid rgb{color}; "
        f"background-color: rgba{color + (0.5,)}'>{effect}</span>"
    )


def style_effects(effects: EffectList) -> str:
    """Return an effect list as HTML."""
    return "<br>".join(get_effect_tag(effect) for effect in effects)


def get_image_tag(ingredient: Optional[Ingredient] = None):
    """Return an ingredient represented as an HTML <img> tag."""
    if ingredient is None:
        image_tag = ""
    else:
        slug = ingredient.name.lower().replace(" ", "_").replace("ñ", "n")
        img_path = Path("app/static") / f"{slug}.png"
        image_tag = (
            f"<img src='{img_path}' style='width: 3rem;' " f"title='{ingredient.name}'>"
        )
    return (
        "<div style='background: rgba(38, 39, 48, 0.8); border-radius: 0.5rem'"
        f">{image_tag}</div>"
    )


def style_ingredients(condiments: list[Condiment], fillings: list[Filling]) -> str:
    """Return an ingredient list as HTML."""
    html = (
        "<div style='display: inline-grid; gap: 0.5rem; "
        "grid-template-columns: repeat(6, 1fr)'>"
    )
    fillings = sorted(fillings)
    for i in range(6):
        html += get_image_tag(fillings[i] if i < len(fillings) else None)
    condiments = sorted(condiments)
    for i in range(4):
        html += get_image_tag(condiments[i] if i < len(condiments) else None)
    html += "</div>"
    return html


def main() -> None:
    st.set_page_config("Sandwich Recipe Suggester", ":sandwich:")

    if "disabled_type" not in st.session_state:
        st.session_state.disabled_type = [False] * 3

    if "rollout_policy_desc" not in st.session_state:
        st.session_state.rollout_policy_desc = ""

    st.title(":sandwich: Recipe Suggester")
    st.subheader("Sandwich Effects")
    cols = st.columns([1, 1, 1])

    for i, col in enumerate(cols):
        with col:
            st.write(f"Effect {i + 1}")
            st.selectbox(
                "Power",
                POWERS,
                key=f"power{i}",
                on_change=update_target_selectboxes,
            )
            st.selectbox(
                "Type",
                TYPES,
                key=f"type{i}",
                disabled=st.session_state.disabled_type[i],
                on_change=update_target_selectboxes,
            )

    with st.expander("Advanced options"):
        num_iter = int(
            st.number_input(
                "Number of trees",
                value=10,
                help=(
                    "Number of trees to generate and explore. Note that only "
                    "trees that exactly match the target effects are recorded"
                ),
            )
        )
        exploration_constant = st.number_input(
            "Exploration constant",
            value=1.0,
            step=0.1,
            help="Bias of the algorithm towards exploration of less tried ingredients",
        )
        max_walltime = st.number_input(
            "Max. decision time (ms)",
            value=1000,
            step=100,
            help=(
                "Maximum time (in ms) the algorithm has to choose an ingredient, "
                "meaning the maximum time to generate a ten-ingredient sandwich "
                "is this number times ten"
            ),
        )
        rollout_policy_name = st.selectbox(
            "Rollout policy",
            [
                name[0].upper() + name[1:].replace("_", " ")
                for name in p.ROLLOUT_POLICIES.keys()
            ],
            help="Policy used to randomly pick an ingredient to add to the sandwich",
            key="rollout_policy",
            on_change=change_rollout_policy_desc,
        )
        st.caption("Rollout policy explanation")
        st.write(st.session_state.rollout_policy_desc)
        change_rollout_policy_desc()
        rollout_policy_func = get_rollout_policy_func(rollout_policy_name)

    if st.button("Suggest recipes"):
        try:
            targets = parse_targets()
        except (e.UnexpectedPower, e.UnexpectedType) as exception:
            st.error(str(exception))
        else:
            pbar_text = "Operation in progress. Please wait."
            pbar = st.progress(0.0, pbar_text)

            mcts_kwargs = dict(
                rollout_policy=rollout_policy_func,
                exploration_constant=exploration_constant / sqrt(2),
                max_walltime=max_walltime,
            )

            rows = []
            placeholder = st.empty()

            recipe_gen = RecipeGenerator(targets, num_iter, **mcts_kwargs)
            for i, sandwich in enumerate(recipe_gen):
                pbar_val = (i + 1) / num_iter
                pbar.progress(pbar_val, f"Operation in progress. ({i+1}/{num_iter})")

                if not sandwich:
                    continue

                effects_html = style_effects(sandwich.effects)
                ingredients_html = style_ingredients(
                    sandwich.condiments, sandwich.fillings
                )
                score = sandwich.get_reward()
                num_ingredients = len(sandwich.ingredients)

                rows.append((effects_html, ingredients_html, score, num_ingredients))
                df = pd.DataFrame(
                    rows, columns=["Effects", "Ingredients", "Match", "Size"]
                )
                df_html = (
                    df.sort_values(["Match", "Size"], ascending=[False, True])
                    .drop_duplicates(["Ingredients"])
                    .style.format(
                        {"Match": lambda x: f"{min(1.0, cast(float, x)):.3f}"}
                    )
                    .hide(axis="index")
                    .hide(["Size"], axis="columns")
                    .to_html()
                )
                with placeholder.container():
                    st.markdown(df_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
