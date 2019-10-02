#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from collections import Counter
from nrs_lib.nrs_engine.request_parser import request_generator, _request_iterator_


NURSE_COUNT = 3
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
        variables = list(request_generator(NURSE_COUNT, PATIENT_REQUEST))

        """
            54 = 9 (requests) * 3(nurses) * 2(nodes)
            54   = 3(days) * 3(nurses) * 3(patients) * 2(start and return)  
            ---
            108
        """
        self.assertEqual(len(variables), 108)

        """
            Patient 1 and 3 request for service on day
            1
        """
        for i in range(NURSE_COUNT):
            self.assertIn((1, i, 0, 1, True), variables)
            self.assertIn((1, i, 1, 0, True), variables)
            self.assertIn((1, i, 0, 3, True), variables)
            self.assertIn((1, i, 3, 0, True), variables)
            self.assertIn((1, i, 3, 1, True), variables)
            self.assertIn((1, i, 1, 3, True), variables)


        """
            Patients 1 and 3 does not request service 
            on day 0
        """
        for i in range(NURSE_COUNT):
            self.assertIn((0, i, 0, 1, False), variables)
            self.assertIn((0, i, 1, 0, False), variables)
            self.assertIn((0, i, 0, 3, False), variables)
            self.assertIn((0, i, 3, 0, False), variables)
            self.assertIn((0, i, 3, 1, False), variables)
            self.assertIn((0, i, 1, 3, False), variables)

        #ensure uniqueness
        counter = Counter(variables)
        for k, v in counter.items():
            self.assertEqual(v, 1, k)

        """
            each tuple contatins
            (day, nurse, from, to, Pass)
            pass is a boolean
        """
        for var in variables:
            self.assertEqual(len(var), 5)

if __name__ == "__main__":
    unittest.main()
