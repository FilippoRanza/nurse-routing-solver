#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, subtour_elimination
from .build_result import build_nurse_result, debug_output, build_external_result
from .request_parser import days_count, constraint_generator
from .service_parser import service_parser


def clean_solution(transit, epsilon):
    for k, v in transit:
        val = v.getAttr('x')
        if val > (1 - epsilon):
            v.setAttr('x')

def run_solver(config, debug):

    model_config = ModelConfigurator("Name")
    transit = constraint_generator(config["PATIENTS"])
    model_config.set_variables(
        config["NURSES"],
        len(config["PATIENTS"]),
        days_count(config["PATIENTS"]),
        transit,
    )
    model_config.set_objective(
        config["HUB_DISTANCE"], config["PATIENTS_DISTANCE"], 5000, 0.1
    )

    service_time = service_parser(
        config["PATIENTS"], config["SERVICES"], config["BASE_TIME_SLOT"]
    )

    model_config.set_time_constraint(
        config["NURSES_WORK_TIME"],
        config["HUB_DISTANCE"],
        config["PATIENTS_DISTANCE"],
        0.01,
        service_time,
    )

    model, transit, patients = model_config.get_model()

    model.optimize(subtour_elimination)

    if debug:
        debug_output(transit)

    return build_nurse_result(transit), build_external_result(patients)
