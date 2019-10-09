#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from nrs_lib.nrs_engine.instance_size import instance_size
from nrs_lib.nrs_io.load_instance import instance_obj


class TestInstanceSize(unittest.TestCase):
    def test_instance_size(self):
        nurses = 4
        days = 3
        patients = 5
        inst = instance_obj(
            nurses=nurses,
            nurse_work=1,
            hub_distances=[],
            patient_distances=[],
            services=[],
            patients=[[0 for _ in range(days)] for _ in range(patients)],
            base_time=0,
        )

        self.assertEqual(nurses * days * patients, instance_size(inst))


if __name__ == "__main__":
    unittest.main()
