#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from nrs_lib import *


def compute_timeout(args, instance):
    if args.tmax:
        return args.tmax
    elif args.auto:
        return args.auto * instance_size(instance)
    return 0


def main():
    args = parse_args()
    instance = parse_instance(args.instance)
    config = get_conf(args.config)
    tmax = compute_timeout(args, instance)
    answer = run_solver(instance, config, args.debug, tmax, args.gap)

    if args.clean:
        cleanup()

    output_result(answer, args.output, args.verbose, args.name)


if __name__ == "__main__":
    main()
