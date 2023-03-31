__all__ = ["ingredient_data"]

from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from pokemon_gourmet.enums import Flavor, Power, Type
from pokemon_gourmet.singleton import Singleton


class IngredientData(metaclass=Singleton):
    def __init__(self) -> None:
        data_path = Path(__file__).parent / "ingredient_data.csv"
        data = pd.read_csv(data_path, index_col=0)

        self.num_ingredients = len(data)
        self.power_mat: NDArray[np.intp] = data[Power._member_names_].to_numpy()
        self.flavor_mat: NDArray[np.intp] = data[Flavor._member_names_].to_numpy()
        self.type_mat: NDArray[np.intp] = data[Type._member_names_].to_numpy()

        self.names: list[str] = data.index.tolist()

        self.pieces: NDArray[np.intp] = data["pieces"].to_numpy()

        self.is_condiment: NDArray[np.bool_] = data["is_condiment"].to_numpy()
        self.is_filling = ~self.is_condiment
        self.is_herba_mystica: NDArray[np.bool_] = data["is_herba_mystica"].to_numpy()

    def __getitem__(self, idx: int) -> str:
        return self.names[idx]

    def __len__(self) -> int:
        return self.num_ingredients

    def index(self, key: str) -> int:
        return self.names.index(key)


ingredient_data = IngredientData()
