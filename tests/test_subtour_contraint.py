#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import unittest
from nrs_lib.subtour_constraint import find_tours, find_subtour


class TestSubtourBuiler(unittest.TestCase):
    def test_subtour(self):
        nodes = [(0, 1), (1, 0), (3, 4), (4, 5), (5, 3)]
        subtour = find_subtour(nodes)
        self.assertEqual(subtour, [(0, 1), (1, 0)])
        self.assertEqual(nodes, [(3, 4), (4, 5), (5, 3)])

    def test_build_tours(self):
        nodes = [(0, 1), (1, 0), (3, 4), (4, 5), (5, 3)]
        tours = list(find_tours(nodes))
        self.assertEqual(len(tours), 1)
        self.assertIn([(3, 4), (4, 5), (5, 3)], tours)


if __name__ == "__main__":
    unittest.main()
