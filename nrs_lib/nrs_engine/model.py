#! /usr/bin/python


# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

try:
    from gurobipy import *
except ImportError:
    print("this error is silenced for testing purpose")
from .build_distance import build_distance
from .subtour_constraint import find_tours


def arange(size):
    return list(range(size))


class ModelConfigurator:
    def __init__(self, name):
        self.model = Model(name)
        self.distances = None

    def set_variables(self, nurse_count, patient_count, days, request_constraints):
        self.nurses = arange(nurse_count)
        # one node for the ospital
        self.nodes = arange(patient_count + 1)
        self.days = arange(days)

        transit_vars = (
            (d, n, i, j)
            for d in self.days
            for n in self.nurses
            for i in self.nodes
            for j in self.nodes
        )
        self.transit_vars = self.model.addVars(
            ((d, n, i, j) for d, n, i, j in transit_vars),
            name="transit",
            vtype=GRB.BINARY,
        )

        service_key = ((i, n) for i in self.nodes[1:] for n in self.nurses)
        self.service_vars = self.model.addVars(
            service_key, name="service", vtype=GRB.BINARY
        )

        self.patient_vars = self.model.addVars(
            self.nodes[1:], name="patient", vtype=GRB.BINARY
        )

        self._apply_contrains_(request_constraints)

    def _apply_contrains_(self, request_contraints):
        for i in self.nodes[1:]:
            self.model.addConstr(
                self.service_vars.sum(i, "*") == (1 - self.patient_vars[i])
            )

        nodes = request_contraints.node_constaints
        hubs = request_contraints.hub_constaints


        for d, p, r in nodes:
            for n in self.nurses:        
                if r:
                    self.model.addConstr(
                        self.transit_vars.sum(d, n, p, "*")  == self.service_vars.sum(p, n)
                    )
                    self.model.addConstr(
                        self.transit_vars.sum(d, n, "*", p)  == self.service_vars.sum(p, n)
                    )
                else:
                    self.model.addConstr(
                        self.transit_vars.sum(d, n, p, '*') == 0
                    )
                    self.model.addConstr(
                        self.transit_vars.sum(d, n, "*", p) == 0
                    )


    def set_time_constraint(self, tmax, hub_dist, pat_dist, time_conv, service_time):
        distances = self._distances_(hub_dist, pat_dist)
        for d in self.days:
            for n in self.nurses:
                self.model.addConstr(
                    (time_conv * (self.transit_vars.prod(distances, d, n, "*", "*")))
                    + (
                        quicksum(
                            service_time[i][d] * self.service_vars.sum(i, n)
                            for i in self.nodes[1:]
                        )
                    )
                    <= tmax
                )

    def set_objective(self, hub_distances, patient_distances, external, transit):

        distances = self._distances_(hub_distances, patient_distances)

        self.model.setObjective(
            (transit * self.transit_vars.prod(distances))
            + (external * self.patient_vars.sum())
        )

    def get_model(self):
        setattr(self.model, "_transit", self.transit_vars)
        setattr(self.model, "_nurses", self.nurses)
        setattr(self.model, "_patient_count", len(self.nodes))
        setattr(self.model, "_days", self.days)
        self.model.Params.lazyConstraints = 1

        return self.model, self.transit_vars, self.patient_vars

    def _distances_(self, hub, pat):
        if self.distances is None:
            distances = build_distance(hub, pat, 1000)
            self.distances = {
                (day, k, f, t): d
                for f, dist in enumerate(distances)
                for t, d in enumerate(dist)
                for k in self.nurses
                for day in self.days
            }

        return self.distances


def subtour_elimination(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._transit)
        for d in model._days:
            for k in model._nurses:
                selected = tuplelist(
                    (i, j)
                    for _, _, i, j in model._transit.keys().select(d, k, "*", "*")
                    if vals[d, k, i, j] >= 0.5
                )

                for tour in find_tours(selected):
                    model.cbLazy(
                        quicksum(model._transit[d, k, i, j] for i, j in tour)
                        <= len(tour) - 1
                    )
