#!/bin/env python3
# -*- coding: utf-8 -*-
# sorts structured data files according to a sorting definition
# usage: python3 ssort.py <input_file> <sorting_definition> [<output_file>]

# Imports
from ruamel.yaml import YAML
import json
from collections import OrderedDict

import re

import argparse
import sys


def sort_level(level, sorting):
    '''
    sorts one level of a structured file according to it's sorting definition
    '''
    #syntactic sugar for sorting when only "by" entry is required in the sorting definition
    if isinstance(sorting, str):
        #pattern for element value sorting
        element_pattern = re.compile('element.(?P<value>.*)')
        if sorting == 'none':
            return level
        elif sorting == 'key':
            return sort_level_key(level)
        elif sorting == 'value':
            return sort_level_value(level)
        elif element_pattern.match(sorting):
            value = element_pattern.match(sorting).group('value')
            return sort_level_element(level, value)

    #syntactic sugar for sorting in a custom order when only "order" entry is required in the sorting definition
    elif isinstance(sorting, list):
        return sort_level_order(level, sorting)

    #default way of defining a sorting order
    if sorting['by'] == 'none':
        return level
    elif sorting['by'] == 'key':
        return sort_level_key(level)
    elif sorting['by'] == 'value':
        return sort_level_value(level)
    elif sorting['by'] == 'element':
        return sort_level_element(level, sorting['value'])
    elif sorting['by'] == 'custom':
        return sort_level_order(level, sorting['order'])

def sort_level_key(level):
    '''
    sorts a dictionary by its keys and retruns the sorted dictionary
    '''
    if isinstance(level, list): return sort_level_value(level)
    level_sorted = dict(sorted(level.items(), key=lambda x: x[0].lower()))
    return level_sorted

def sort_level_value(level):
    '''
    sorts a list alphabetically and returns the sorted list
    sorts a dictionary by it's value if each dictionary key has a stringifiably sortable single value, otherwise sorts by key
    '''
    if isinstance(level, list):
        for value in level:
            if isinstance(value, dict) or isinstance(value, list):
                return level
        level_sorted = sorted(level, key=lambda x: str(x).lower())
        return level_sorted
    elif isinstance(level, dict):
        for key in level:
            if isinstance(level[key], list) or isinstance(level[key], dict):
                return sort_level_key(level)
        return dict(sorted(level.items(), key=lambda x: str(x[1]).lower()))

def sort_level_element(level, element):
    '''
    sorts a list or dictionary of dictionaries by a specific element and returns the sorted list
    '''
    if isinstance(level, list) or isinstance(level, dict):
        for child in level:
            if not isinstance(child, dict):
                return level
        level_sorted = sorted(filter(lambda x: element in x, level), key=lambda x: str(x[element]).lower())
        #add the rest of the elements to the sorted list
        for child in level:
            if child not in level_sorted:
                level_sorted.append(child)
        if isinstance(level, list):
            return level_sorted
        else:
            return dict(level_sorted)

def sort_level_order(level, order):
    '''
    sorts a dictionary with a specific order of keys and returns the sorted dictionary
    any keys not defined in the order are kept in the same order as they were in the original dictionary
    '''
    if not isinstance(level, dict): return level
    level_sorted = {}
    for key in order:
        if key in level:
            level_sorted[key] = level[key]
    for key in level.keys():
        if key not in level_sorted:
            level_sorted[key] = level[key]
    return level_sorted

def recursive_sort(level, sorting_definition):
    '''
    recursively sorts a structures file according to its sorting definition
    '''
    #print('recursive_sort:\n' + str(level) + '\n' + str(sorting_definition) + '\n\n')
    #return if level is not a dictionary or list
    if not isinstance(level, dict) and not isinstance(level, list):
        return level

    #if the sorting definition has an all entry
    #sort all of the children and their children recursively
    if 'all' in sorting_definition:
        #if level is a dictionary
        if isinstance(level, dict):
            new_sorting_definition = sorting_definition['all']
            new_sorting_definition['all'] = sorting_definition['all']
            for key in level:
                level[key] = recursive_sort(level[key], new_sorting_definition)

    #if the sorting definition has an each entry
    #sort each key of the dictionary/ each index of the list
    if 'each' in sorting_definition:
        #if level is a dictionary
        if isinstance(level, dict):
            for key in level:
                level[key] = recursive_sort(level[key], sorting_definition['each'])
        #if level is a list
        elif isinstance(level, list):
            for i in range(len(level)):
                level[i] = recursive_sort(level[i], sorting_definition['each'])
   
    #if the level is a dictionary
    if isinstance(level, dict):
        #for each key check if it has a specific sorting definition
        for key in level:
            if key in sorting_definition:
                level[key] = recursive_sort(level[key], sorting_definition[key])
    
    #check if this level has a sort entry
    if 'sort' in sorting_definition:
        sorting = sorting_definition['sort']
        level = sort_level(level, sorting)
    return level

def load_json(filename):
    '''
    loads a json file and returns the OrderedDict
    '''
    with open(filename) as f:
        return json.load(f, object_pairs_hook=OrderedDict)

def load_yaml(filename):
    '''
    loads a yaml file and returns the OrderedDict
    '''
    with open(filename) as f:
        return YAML().load(f)

def write_json(filename, data):
    '''
    writes a json file
    '''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def write_yaml(filename, data):
    '''
    writes a yaml file
    '''
    with open(filename, 'w') as f:
        YAML().dump(data, f)

def load_file(filename):
    '''
    loads a file and returns the OrderedDict
    '''
    if filename.endswith('.json'):
        return load_json(filename)
    elif filename.endswith('.yaml'):
        return load_yaml(filename)
    else:
        print('unsupported file format')
        sys.exit(1)

def write_file(filename, data):
    '''
    writes a file
    '''
    if filename.endswith('.json'):
        write_json(filename, data)
    elif filename.endswith('.yaml'):
        write_yaml(filename, data)
    else:
        print('unsupported file format')
        sys.exit(1)



if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Sorts structured data files according to a sorting definition')
    parser.add_argument('input_file', help='input file')
    parser.add_argument('sorting_definition', help='sorting definition file')
    parser.add_argument('output_file', nargs='?', help='output file')
    args = parser.parse_args()

    # Read sorting definition
    sorting_definition = load_file(args.sorting_definition)

    # Load input file
    data = load_file(args.input_file)

    # Sort yaml file
    data = recursive_sort(data, sorting_definition)

    # if output file is not given, write to input file
    if not args.output_file:
        args.output_file = args.input_file

    # Write output
    write_file(args.output_file, data)
    
    # done
    print('done')
    sys.exit(0)
