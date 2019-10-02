#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def _get_services(requests, services):
    for i in requests:
        if i:
            yield services[i - 1]
        else:
            yield 0



def _service_time(services, base_time):
    tmp = map(lambda i: i * base_time, services)
    return list(tmp)


def service_parser(patient_request, services, base_time):
    services = _service_time(services, base_time)
    out = {}
    for pat, pat_req in enumerate(patient_request, 1):
        req = pat_req["REQUEST"]
        ser = list(_get_services(req, services))
        out[pat] = ser

    return out
