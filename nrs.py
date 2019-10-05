#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from nrs_lib import *


def main():
    args = parse_args()
    instance = load_instance(args.instance)
    nurses, external = run_solver(instance, args.debug, args.tmax, args.gap)

    if args.clean:
        cleanup()

    output_result(nurses, external, args.output)


if __name__ == "__main__":
    main()
