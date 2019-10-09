#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from .model import ModelConfigurator, gurobi_callback
from .build_result import build_nurse_result, debug_output, build_external_result
from .request_parser import days_count, constraint_generator
from .service_parser import service_parser


def run_solver(instance, config, debug, max_time, min_gap):

    model_config = ModelConfigurator("Name")
    transit = constraint_generator(instance.patients)
    model_config.set_variables(
        instance.nurses, len(instance.patients), days_count(instance.patients), transit
    )
    model_config.set_objective(
        instance.hub_distances,
        instance.patient_distances,
        config.external_cost,
        config.transfer_cost,
    )

    service_time = service_parser(
        instance.patients, instance.services, instance.base_time
    )

    model_config.set_time_constraint(
        instance.nurse_work,
        instance.hub_distances,
        instance.patient_distances,
        config.transfer_speed,
        service_time,
    )

    model, transit, patients = model_config.get_model()

    model.optimize(gurobi_callback(max_time, min_gap))

    if debug:
        debug_output(model)

    return build_nurse_result(transit), build_external_result(patients)
