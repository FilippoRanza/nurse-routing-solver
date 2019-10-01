#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def days_count(config):
    head = config[0]
    req = head["REQUEST"]
    return len(req)


def _gen_variables_(day, request, patient, nurses, patients):
    if not request:
        for n in nurses:
            for p in patients[patient - 1:]:
                if p != patient:
                    yield day, n, patient, p
                    yield day, n, p, patient


def _request_iterator_(patient_requests):
    for pat, requests in enumerate(patient_requests, 1):
        for day, req in enumerate(requests['REQUEST']):
            yield day, pat, req

def _hub_iterator_(d, nurses, patient, request):
    if not request:
        for n in nurses:
            yield d, n, 0, patient
            yield d, n, patient, 0
    
    


def request_generator(nurse_count, patient_request):
    nurses = list(range(nurse_count))
    patients = list(range(1, len(patient_request) + 1))
    for d, p, r in _request_iterator_(patient_request):
        yield from _gen_variables_(d, r, p, nurses, patients)
        yield from _hub_iterator_(d, nurses, p, r)