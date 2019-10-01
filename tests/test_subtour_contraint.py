#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from nrs_lib.nrs_engine.subtour_constraint import find_tours, find_subtour


class TestSubtourBuiler(unittest.TestCase):
    def test_subtour(self):
        nodes = [(0, 7), (2, 5), (4, 6), (5, 4), (6, 2), (7, 0)]
        subtour = find_subtour(nodes)
        self.assertEqual(subtour, [(0, 7), (7, 0)])
        self.assertEqual(nodes, [(2, 5), (4, 6), (5, 4), (6, 2)])

    def test_build_tours(self):
        nodes = [(0, 7), (2, 5), (4, 6), (5, 4), (6, 2), (7, 0)]
        tours = list(find_tours(nodes))
        self.assertEqual(len(tours), 1)
        self.assertIn([(2, 5), (5, 4), (4, 6), (6, 2)], tours)


if __name__ == "__main__":
    unittest.main()
