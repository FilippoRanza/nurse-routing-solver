#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from argparse import ArgumentParser

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

    return parser.parse_args()