#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from collections import Counter
from nrs_lib.nrs_engine.request_parser import constraint_generator, _request_iterator_


PATIENT_REQUEST = [
    {"ID": (883, 527), "REQUEST": [0, 3, 0]},
    {"ID": (353, 550), "REQUEST": [3, 0, 3]},
    {"ID": (711, 641), "REQUEST": [0, 2, 0]},
]


class TestRequestParser(unittest.TestCase):
    def test_request_iterator(self):
        answer = list(_request_iterator_(PATIENT_REQUEST))
        self.assertEqual(len(answer), 9)

        correct_ans = [
            (0, 1, 0),
            (1, 1, 3),
            (2, 1, 0),
            (0, 2, 3),
            (1, 2, 0),
            (2, 2, 3),
            (0, 3, 0),
            (1, 3, 2),
            (2, 3, 0),
        ]

        self.assertEqual(correct_ans, answer)

    def test_request_generator(self):
        constraints =constraint_generator(PATIENT_REQUEST)

        nodes = list(constraints.node_constaints)
        hub = list(constraints.hub_constaints)


        """
            9, the combinations of all requests
        """
        self.assertEqual(len(nodes), len(hub))
        self.assertEqual(nodes, hub)
        self.assertEqual(len(nodes), 9)

        #ensure uniqueness
        counter = Counter(nodes)
        for k, v in counter.items():
            self.assertEqual(v, 1, k)

        """
            each tuple contatins
            (day, nurse, from, to, Pass)
            pass is a boolean
        """
        for var in nodes:
            self.assertEqual(len(var), 3)
            self.assertIn(var[2], [0, 1])

if __name__ == "__main__":
    unittest.main()
