#! /usr/bin/python

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import json
from os import remove


CLEAN_FILES = ["gurobi.log"]


def load_instance(file_name):
    with open(file_name) as data:
        out = json.load(data)
    return out


def cleanup():
    for f in CLEAN_FILES:
        try:
            remove(f)
        except:
            pass
