#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest

from nrs_lib.nrs_engine.service_parser import service_parser, _service_time


PATIENT_REQUEST = [
    {"ID": (883, 527), "REQUEST": [0, 3, 0]},
    {"ID": (353, 550), "REQUEST": [3, 0, 3]},
    {"ID": (711, 641), "REQUEST": [0, 2, 0]},
]


SERVICES = [8, 1 ,5]
BASE_TIME = 15

class TestServiceParser(unittest.TestCase):

    def test_service_time(self):
        services = _service_time(SERVICES, BASE_TIME)
        self.assertIsInstance(services, list)
        self.assertEqual(len(services), len(SERVICES))
        self.assertEqual(services, [120, 15, 75])

    def test_service_parser(self):
        services = service_parser(PATIENT_REQUEST, SERVICES, BASE_TIME)
        self.assertIsInstance(services, dict)
        self.assertEqual(len(services), len(PATIENT_REQUEST))
        self.assertEqual(services, {1: 75, 2: 75, 3: 15})

if __name__ == "__main__":
    unittest.main()