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
    path = {}
    for k, v in variables.items():
        val = v.getAttr("x")
        if val:
            n, i, j = k
            try:
                path[n].append((i, j))
            except KeyError:
                path[n] = [(i, j)]

    out = {k: build_path(v) for k, v in path.items()}

    return out
