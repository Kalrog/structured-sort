#!/bin/env python3
# -*- coding: utf-8 -*-
# sorts structured data files according to a sorting definition
# usage: python3 ssort.py <input_file> <sorting_definition> [<output_file>]

# Imports
from ruamel.yaml import YAML
import json
from collections import OrderedDict

import argparse
import sys


def sort_level(level, sorting):
    '''
    sorts one level of a structured file according to it's sorting definition
    '''
    #if sorting is a string
    if isinstance(sorting, str):
        if sorting == 'none':
            return level
        elif sorting == 'key':
            return sort_level_key(level)
    elif isinstance(sorting, dict):
        sort_by=sorting['by']
        if sort_by == 'value':
            return sort_level_value(level)
        elif sort_by == 'element':
            return sort_level_element(level, sorting['value'])
    elif isinstance(sorting, list):
        return sort_level_order(level, sorting)


def sort_level_key(level):
    '''
    sorts a dictionary by its keys and retruns the sorted dictionary
    '''
    level_sorted = dict(sorted(level.items(), key=lambda x: x[0].lower()))
    return level_sorted

def sort_level_value(level):
    '''
    sorts a list alphabetically and returns the sorted list
    '''
    level_sorted = sorted(level, key=lambda x: x.lower())
    return level_sorted

def sort_level_element(level, element):
    '''
    sorts a list of dictionaries by a specific element and returns the sorted list
    '''
    level_sorted = sorted(level, key=lambda x: x[element].lower())
    return level_sorted

def sort_level_order(level, order):
    '''
    sorts a dictionary with a specific order of keys and returns the sorted dictionary
    any keys not defined in the order list are sorted alphabetically after the defined keys
    '''
    level_sorted = {}
    for key in order:
        if key in level:
            level_sorted[key] = level[key]
    for key in dict(sorted(level.items(), key=lambda x: x[0])):
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
