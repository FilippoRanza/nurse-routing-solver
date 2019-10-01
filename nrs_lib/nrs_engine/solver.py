#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, subtour_elimination
from .build_result import build_nurse_result, debug_output, build_external_result
from .request_parser import days_count, request_generator


def run_solver(config, debug):

    model_config = ModelConfigurator("Name")
    transit = request_generator(config["NURSES"], config["PATIENTS"])
    model_config.set_variables(
        config["NURSES"], len(config["PATIENTS"]), days_count(config["PATIENTS"]), transit
    )
    model_config.set_objective(
        config["HUB_DISTANCE"], config["PATIENTS_DISTANCE"], 5000, 0.1
    )

    model_config.set_time_constraint(
        config["NURSES_WORK_TIME"],
        config["HUB_DISTANCE"],
        config["PATIENTS_DISTANCE"],
        0.1,
    )

    model, transit, patients = model_config.get_model()

    model.optimize(subtour_elimination)

    if debug:
        debug_output(transit)

    return build_nurse_result(transit), build_external_result(patients)
