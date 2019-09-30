#! /usr/bin/python3

from argparse import ArgumentParser
import json
from os import remove

from nrs_lib import run_solver

CLEAN_FILES = ['gurobi.log']

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("instance", help="Request file")
    parser.add_argument("-o", "--output", help="Specify output file")
    parser.add_argument('-c', '--clean', action='store_true',
                        default=False, help='Remove gurobi.log after model optimization')

    return parser.parse_args()


def load_instance(file_name):
    with open(file_name) as data:
        out = json.load(data)
    return out

def cleanup(files):
    for f in files:
        try:
            remove(f)
        except:
            pass


def main():
    args = parse_args()
    instance = load_instance(args.instance)
    result = run_solver(instance)
    print(result)
    if args.clean:
        cleanup(CLEAN_FILES)


if __name__ == "__main__":
    main()
