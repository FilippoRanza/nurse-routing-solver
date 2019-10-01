#! /usr/bin/python

import unittest
from nrs_lib.nrs_engine.build_distance import build_distance


class TestBuildDistance(unittest.TestCase):
    def test_build_distance(self):
        hub_dist = [34, 45, 56, 23]
        patient_dist = [[0, 12, 23, 3], [12, 0, 34, 21], [23, 34, 0, 6], [3, 21, 6, 0]]

        correct = [
            [168, 34, 45, 56, 23],
            [34, 168, 12, 23, 3],
            [45, 12, 168, 34, 21],
            [56, 23, 34, 168, 6],
            [23, 3, 21, 6, 168],
        ]

        dist_matrix = build_distance(hub_dist, patient_dist, 3)
        self.assertEqual(len(dist_matrix), len(patient_dist) + 1)
        for row in dist_matrix:
            self.assertEqual(len(row), len(patient_dist) + 1)

        self.assertEqual(dist_matrix, correct)


if __name__ == "__main__":
    unittest.main()
