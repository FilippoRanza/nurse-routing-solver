#! /usr/bin/python

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from sys import stdout


def _write_output_(result, fp):
    for day, path in result.items():
        print(f"Day {day}", file=fp)
        print(path, file=fp)


def output_result(result, file_name):
    if file_name:
        with open(file_name, "w") as out:
            _write_output_(result, out)
    else:
        _write_output_(result, stdout)
