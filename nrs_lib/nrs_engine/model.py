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

    def set_variables(self, nurse_count, patient_count, days):
        self.nurses = arange(nurse_count)
        self.nodes = arange(patient_count)
        self.days = arange(days)

        transit_keys = (
            (d, n, i, j)
            for d in self.days
            for n in self.nurses
            for i in self.nodes
            for j in self.nodes
        )
        self.transit_vars = self.model.addVars(
            transit_keys, name="transit", vtype=GRB.BINARY
        )

        service_key = ((i, n) for i in self.nodes[1:] for n in self.nurses)
        self.service_vars = self.model.addVars(
            service_key, name="service", vtype=GRB.BINARY
        )

        self.patient_vars = self.model.addVars(
            self.nodes[1:], name="patient", vtype=GRB.BINARY
        )

        self._apply_contrains_()

    def _apply_contrains_(self):
        for i in self.nodes[1:]:
            self.model.addConstr(
                self.service_vars.sum(i, "*") == (1 - self.patient_vars[i])
            )

        for d in self.days:
            for i in self.nodes[1:]:
                for n in self.nurses:
                    self.model.addConstr(
                        self.transit_vars.sum(d, n, i, "*")
                        == self.service_vars.sum(i, n)
                    )

                    self.model.addConstr(
                        self.transit_vars.sum(d, n, "*", i)
                        == self.service_vars.sum(i, n)
                    )

        for k in self.nurses:
            for d in self.days:
                self.model.addConstr(
                    quicksum(
                        self.service_vars.sum(i, k) * self.transit_vars.sum(d, k, 0, i)
                        for i in self.nodes[1:]
                    )
                    == 1
                )
                self.model.addConstr(
                    quicksum(
                        self.service_vars.sum(i, k) * self.transit_vars.sum(d, k, i, 0)
                        for i in self.nodes[1:]
                    )
                    == 1
                )

    def set_time_constraint(self, tmax, hub_distance, patient_distance, time_conv):
        distances = self._distances_(hub_distance, patient_distance)
        for d in self.days:
            for n in self.nurses:
                self.model.addConstr(
                    (time_conv * (self.transit_vars.prod(distances, d, n, "*", "*")))
                    <= tmax
                )

    def set_objective(self, hub_distances, patient_distances, external, transit):

        distances = self._distances_(hub_distances, patient_distances)

        self.model.setObjective(
            (transit * self.transit_vars.prod(distances))
            + (external * len(self.days) * self.patient_vars.sum())
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
                    if vals[d, k, i, j] > 0.5
                )

                for tour in find_tours(selected):
                    model.cbLazy(
                        quicksum(model._transit[d, k, i, j] for i, j in tour)
                        <= len(tour) - 1
                    )
