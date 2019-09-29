#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigutator, subtour_elimination
from .build_result import build_result


def run_solver(config):

    model_config = ModelConfigutator("Name")
    model_config.set_variables(config["NURSES"], len(config["PATIENTS"]))
    model_config.set_objective(
        config["HUB_DISTANCE"], config["PATIENTS_DISTANCE"], 10000
    )

    model, transit = model_config.get_model()

    model.optimize(subtour_elimination)

    return build_result(transit)
