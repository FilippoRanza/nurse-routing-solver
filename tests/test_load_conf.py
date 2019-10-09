#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from tempfile import TemporaryDirectory
from os.path import join
from nrs_lib.nrs_io.run_config import get_conf, DEFAULT_CONF

EXAMPLE_CONFIG = """
PETROL_PRICE: 1.6
CONSUMPTION: 7.5
DISTANCE_FACTOR: 10
AVERAGE_SPEED: 45
EXTERNAL_COST: 100
"""


class TestConf(unittest.TestCase):
    def test_get_conf(self):
        conf = get_conf(None)
        self.assertEqual(conf, DEFAULT_CONF)

    def test_base_parse(self):
        with TemporaryDirectory() as path:
            file = join(path, "conf.yml")
            with open(file, "w") as out:
                print(EXAMPLE_CONFIG, file=out)

            conf = get_conf(file)
            self.assertEqual(len(conf), 3)
            self.assertAlmostEqual((1.6 * 7.5) / (10 ** 4), conf.transfer_cost)
            self.assertEqual(conf.external_cost, 100)
            self.assertAlmostEqual(conf.transfer_speed, 1 / ((45 * (50 / 3)) / 10))

    def test_correct_result(self):
        with TemporaryDirectory() as path:
            file = join(path, "conf.yml")
            with open(file, "w") as out:
                print(EXAMPLE_CONFIG, file=out)

            conf = get_conf(file)
            # 10000 dM is 100Km
            self.assertAlmostEqual(conf.transfer_cost * 10000, 1.6 * 7.5)
            # 4500 dM is 45 Km
            self.assertAlmostEqual(conf.transfer_speed * 4500, 60)


if __name__ == "__main__":
    unittest.main()
