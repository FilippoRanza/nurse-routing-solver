#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, gurobi_callback
from .build_result import build_nurse_result, debug_output, build_external_result
from .request_parser import days_count, constraint_generator
from .service_parser import service_parser


def run_solver(instance, config, debug, max_time, min_gap):

    model_config = ModelConfigurator("Name")
    transit = constraint_generator(instance["PATIENTS"])
    model_config.set_variables(
        instance["NURSES"],
        len(instance["PATIENTS"]),
        days_count(instance["PATIENTS"]),
        transit,
    )
    model_config.set_objective(
        instance["HUB_DISTANCE"], instance["PATIENTS_DISTANCE"], config.external_cost, config.transfer_cost
    )

    service_time = service_parser(
        instance["PATIENTS"], instance["SERVICES"], instance["BASE_TIME_SLOT"]
    )

    model_config.set_time_constraint(
        instance["NURSES_WORK_TIME"],
        instance["HUB_DISTANCE"],
        instance["PATIENTS_DISTANCE"],
        config.transfer_speed,
        service_time,
    )

    model, transit, patients = model_config.get_model()

    model.optimize(gurobi_callback(max_time, min_gap))

    if debug:
        debug_output(model)

    return build_nurse_result(transit), build_external_result(patients)
