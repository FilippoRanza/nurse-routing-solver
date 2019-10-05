#! /usr/bin/python3


# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest

from nrs_lib.nrs_io.arg_parser import time_parser


class TestTimeParser(unittest.TestCase):
    def test_time_parser(self):
        self.assertEqual(time_parser("2:30:00"), 9000)


if __name__ == "__main__":
    unittest.main()
