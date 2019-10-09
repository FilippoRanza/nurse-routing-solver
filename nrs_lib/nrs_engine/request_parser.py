#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def days_count(config):
    head = config[0]
    return len(head)


def _request_iterator_(patient_requests):
    for pat, requests in enumerate(patient_requests, 1):
        for day, req in enumerate(requests):
            yield day, pat, req


def _node_constraints_(patient_requests):
    for d, p, r in _request_iterator_(patient_requests):
        out = 1 if r else 0
        yield d, p, out


def _hub_iterator_(d, nurses, patient, request):
    req = request != 0
    for n in nurses:
        yield d, n, 0, patient, req
        yield d, n, patient, 0, req


def constraint_generator(patient_request):
    tmp = _node_constraints_(patient_request)
    return tmp
