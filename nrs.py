#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from nrs_lib import *


def main():
    args = parse_args()
    instance = parse_instance(args.instance)
    config = get_conf(args.config)
    nurses, external = run_solver(instance, config, args.debug, args.tmax, args.gap)

    if args.clean:
        cleanup()

    output_result(nurses, external, args.output)


if __name__ == "__main__":
    main()
