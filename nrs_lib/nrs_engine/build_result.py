#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def clean_solution(transit, epsilon):
    for k, v in transit.items():
        val = v.getAttr("x")
        if val > (1 - epsilon):
            yield k, True
        elif val < epsilon:
            yield k, False


def build_path(path):
    f, t = path.pop(0)
    out = [f]
    while path:
        for i, j in path:
            if i == t:
                out.append(i)
                path.remove((i, j))
                t = j
                break

    return out + [0]


def build_nurse_result(variables):
    days = {}

    for k, v in clean_solution(variables, 0.1):

        if v:
            d, n, i, j = k

            try:
                day = days[d]
            except KeyError:
                day = {}
                days[d] = day

            try:
                day[n].append((i, j))
            except KeyError:
                day[n] = [(i, j)]

    out = {
        day: {k: build_path(v) for k, v in path.items()} for day, path in days.items()
    }

    return out


def build_external_result(external):
    out = []
    for k, v in external.items():
        value = v.getAttr("x")
        if value:
            out.append(k)
    return out


def debug_output(model):
    variables = model.getVars()
    for v in variables:
        val = v.getAttr("x")
        if val:
            print(v)
