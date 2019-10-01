#! /usr/bin/python

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from sys import stdout


def _write_nurse_path_(result, fp):
    for day, plan in result.items():
        print(f"Day {day}", file=fp)
        for nurse, path in plan.items(): 
            print(f'Nurse {nurse}:', file=fp)
            print(f'\t{path}', file=fp)


def _write_external_serice_(ext, fp):
    print('External Service:', file=fp)
    for p in ext:
        print(f'Patient {p}')

def _output_wrapper_(nurse, external, fp):
    _write_nurse_path_(nurse, fp)
    _write_external_serice_(external, fp)


def output_result(nurse, external, file_name):
    if file_name:
        with open(file_name, "w") as out:
            _output_wrapper_(nurse, external, out)
    else:
        _output_wrapper_(nurse, external, stdout)
