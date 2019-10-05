#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, gurobi_callback
from .build_result import build_nurse_result, debug_output, build_external_result
from .request_parser import days_count, constraint_generator
from .service_parser import service_parser


def run_solver(config, debug, max_time, min_gap):

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
    
   
    model.optimize(gurobi_callback(max_time, min_gap))


    if debug:
        debug_output(model)

    return build_nurse_result(transit), build_external_result(patients)
