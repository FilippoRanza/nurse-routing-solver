#! /usr/bin/python

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from sys import stdout


def _write_nurse_path_(result, fp):
    for day, plan in result.items():
        print(f"Day {day}", file=fp)
        for nurse, path in plan.items():
            print(f"Nurse {nurse}:", file=fp)
            print(f"\t{path}", file=fp)


def _write_external_serice_(ext, fp):
    print("External Service:", file=fp)
    for p in ext:
        print(f"Patient {p}", file=fp)


def _output_wrapper_(nurse, external, fp):
    _write_nurse_path_(nurse, fp)
    _write_external_serice_(external, fp)

def _verbose_out_(value, status, name, fp):
    print(f'Model {name}')
    print(f'Objective Value {value}', file=fp)
    print(f'Optimal: {status}', file=fp)


def output_result(answer, file_name, verbose, name):
    if file_name:
        with open(file_name, "w") as out:
            if verbose:
                _verbose_out_(answer.value, answer.status, name, out)
            _output_wrapper_(answer.nurse, answer.external, out)
    else:
        if verbose:
            _verbose_out_(answer.value, answer.status, name, stdout)
        _output_wrapper_(answer.nurse, answer.external, stdout)
