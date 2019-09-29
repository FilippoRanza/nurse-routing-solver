#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import define_model, subtour_elimination
from .build_result import build_result


def run_solver(config):

    model, transit = define_model(
        "Name",
        len(config["PATIENTS"]),
        config["NURSES"],
        config["HUB_DISTANCE"],
        config["PATIENTS_DISTANCE"],
        config["NURSES_WORK_TIME"],
    )
    model.Params.lazyConstraints = 1
    model.optimize(subtour_elimination)

    return build_result(transit)
