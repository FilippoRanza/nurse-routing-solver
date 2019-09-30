#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, subtour_elimination
from .build_result import build_result


def days_count(config):
    head = config['PATIENTS'][0]
    req = head['REQUEST']
    return len(req)


def run_solver(config):

    model_config = ModelConfigurator("Name")
    model_config.set_variables(config["NURSES"], len(config["PATIENTS"]), days_count(config))
    model_config.set_objective(
        config["HUB_DISTANCE"], config["PATIENTS_DISTANCE"], 100000
    )

    model, transit = model_config.get_model()

    model.optimize(subtour_elimination)

    return build_result(transit)
