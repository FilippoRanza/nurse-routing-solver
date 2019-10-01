#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


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


def build_result(variables):
    days = {}

    for k, v in variables.items():
        val = v.getAttr("x")
        if val:
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


def debug_output(variables):
    for k, v in variables.items():
        val = v.getAttr("x")
        if val:
            d, n, i, j = k
            print(f"Day {d} - Nurse {n} -> ({i}, {j})")
