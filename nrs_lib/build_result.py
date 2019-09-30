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
                days[d][n].append((i, j))
            except KeyError:
                days[d] = {}
                days[d][n] = [(i, j)]

    out = {day : 
        {k: build_path(v) for k, v in path.items()}
        for day, path in days.items()
        }

    return out
