#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from nrs_lib import *


def main():
    args = parse_args()
    instance = load_instance(args.instance)
    nurses, external = run_solver(instance, args.debug)

    if args.clean:
        cleanup(CLEAN_FILES)

    output_result(nurses, external, args.output)


if __name__ == "__main__":
    main()
