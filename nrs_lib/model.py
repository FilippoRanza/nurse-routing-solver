#! /usr/bin/python


# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


from gurobipy import *
from .build_distance import build_distance


def arange(size):
    return list(range(size))


def define_model(name, patient_count, nurse_count, hub_distance, patient_distance):
    model = Model(name)

    nurses = arange(nurse_count)
    nodes = arange(patient_count)

    transit_keys = ((n, i, j) for n in nurses for i in nodes for j in nodes)
    transit_vars = model.addVars(transit_keys, name="transit", vtype=GRB.BINARY)

    service_key = ((i, n) for i in nodes[1:] for n in nurses)
    service_vars = model.addVars(service_key, name="service", vtype=GRB.BINARY)

    patient_vars = model.addVars(nodes[1:], name="patient", vtype=GRB.BINARY)

    for i in nodes[1:]:
        model.addConstr(service_vars.sum(i, "*") == (1 - patient_vars[i]))

    for i in nodes[1:]:
        for n in nurses:
            model.addConstr(transit_vars.sum(n, i, "*") == service_vars.sum(i, n))
            model.addConstr(transit_vars.sum(n, "*", i) == service_vars.sum(i, n))

    for k in nurses:
        model.addConstr(
            quicksum(
                service_vars.sum(i, k) * transit_vars.sum(k, 0, i) for i in nodes[1:]
            )
            == 1
        )
        model.addConstr(
            quicksum(
                service_vars.sum(i, k) * transit_vars.sum(k, i, 0) for i in nodes[1:]
            )
            == 1
        )

    distances = build_distance(hub_distance, patient_count)

    arch_weight = {
        (k, f, t): d
        for f, dist in enumerate(distances)
        for t, d in enumerate(dist)
        for k in nurses
    }

    beta = 10000
    model.setObjective(transit_vars.prod(arch_weight) + (beta * patient_vars.sum()))

    setattr(model, "_transit", transit_vars)
    setattr(model, "_nurses", nurses)
    setattr(model, "_patient_count", len(nodes))

    return model, transit_vars
