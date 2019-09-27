#! /usr/bin/python3

import unittest
from nrs_lib.subtour_constraint import *


class TestSubtourBuiler(unittest.TestCase):
    
    def test_subtour(self):
        nodes = [(0, 1), (1, 0), (3, 4), (4, 5), (5, 3)]
        subtour = find_subtour(nodes)
        self.assertEqual(subtour, [(0, 1), (1, 0)])
        self.assertEqual(nodes, [(3, 4), (4, 5), (5, 3)])



if __name__ == "__main__":
    unittest.main()