#!/bin/env python3
# unit tests for structured file sorting

import unittest
from ssort import sort_level_key, sort_level_value, sort_level_element, sort_level_order, recursive_sort
from collections import OrderedDict


class TestSortLevel(unittest.TestCase):

    def test_sort_level_key(self):

        level ={'b': '2', 'a': '1', 'c': '3'}
        self.assertEqual(sort_level_key(level), {'a': '1', 'b': '2', 'c': '3'})

        level = OrderedDict(
            {'4': {'b': '2', 'a': '1', 'c': '3'}, "abc": [2, 1, 3], "2": 6})
        self.assertEqual(sort_level_key(level), OrderedDict(
            {'2': 6, '4': {'b': '2', 'a': '1', 'c': '3'}, 'abc': [2, 1, 3]}))

        level = ['a', '543', '+523', '54', 'b', 'c']
        self.assertEqual(sort_level_key(level), [
                         '+523', '54', '543', 'a', 'b', 'c'])

    def test_sort_level_value(self):

        level = ['b', 'a', 'c']
        self.assertEqual(sort_level_value(level), ['a', 'b', 'c'])

        level = ['a', '543', '+523', '54', 'b', 'c']
        self.assertEqual(sort_level_value(level), [
                         '+523', '54', '543', 'a', 'b', 'c'])

        level = {'a': '2', 'b': '1', 'c': '3'}
        self.assertEqual(sort_level_value(level), {
                         'b': '1', 'a': '2', 'c': '3'})

    def test_sort_level_element(self):
        key = 'a'
        level = [{key: 'b'},
            {key: 'a'}, {key: 'c'}]
        self.assertEqual(sort_level_element(level, key), [
            {key: 'a'}, {key: 'b'}, {key: 'c'}])

        level = [{key: 'b', 'd': 'e'},
                 {key: 'a', 'd': 'f'}, {key: 'c', 'd': 'g'}]
        self.assertEqual(sort_level_element(level, key), [
            {key: 'a', 'd': 'f'}, {key: 'b', 'd': 'e'}, {key: 'c', 'd': 'g'}])
        self.assertEqual(sort_level_element(level, 'd'), level)

        level = {'first': {key: 'b', 'd': 'e'}, 'unsorted': {
            'd': 'f'}, 'second': {key: 'c', 'd': 'g'}}
        self.assertEqual(sort_level_element(level, key), {'first': {
                         key: 'b', 'd': 'e'}, 'second': {key: 'c', 'd': 'g'}, 'unsorted': {'d': 'f'}})

    def test_sort_level_order(self):
        order = ['b', 'a', 'c']
        level = {'a': '1', 'b': '2', 'c': '3'}
        self.assertEqual(sort_level_order(level, order),
                        {'b': '2', 'a': '1', 'c': '3'})

        order = ['first', 'second', 'third']
        level = {'second': [3, 2, 1], 'first': [
                            1, 2, 3], 'third': [2, 3, 1]}
        self.assertEqual(sort_level_order(level, order),
            {'first': [1, 2, 3], 'second': [3, 2, 1], 'third': [2, 3, 1]})


if __name__ == '__main__':
    unittest.main()
