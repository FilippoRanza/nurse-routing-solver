#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def instance_size(instance):
    reqs = len(instance.patients[0])
    pats = len(instance.patients)
    nurs = instance.nurses
    return reqs * pats * nurs

