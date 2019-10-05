#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from argparse import ArgumentParser


def time_parser(time_str):
    out = 0
    for token in map(int, time_str.split(":")):
        out *= 60
        out += token

    return out


def percentage_parser(percent_str):
    num = float(percent_str)
    if num >= 1:
        num /= 100
    return num


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--instance", help="Request file")
    parser.add_argument("-o", "--output", help="Specify output file")
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        default=False,
        help="Remove gurobi.log after model optimization",
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="Enable debug mode"
    )

    parser.add_argument(
        "--gap",
        help="""Specify the desidered gap between the current
        solution and the LP relaxation. When this gap is reached the
        execution is stopped
        and the current best result is returned. If this option is 
        used with --tmax the gap stop is enabled only after tmax has
        elapse. By default gap stop is not enabled""",
        type=percentage_parser,
    )

    parser.add_argument(
        "--tmax",
        help="""Specify maximum execution time, if the solver
        does not find a solution in this time the execution is stopped
        and the current best result is returned. If this option is 
        used with --gap the gap stop is enabled only after tmax has
        elapse. By default tmax is set to infinity""",
        type=time_parser,
    )

    return parser.parse_args()
