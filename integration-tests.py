#!/bin/env python3
# integration tests for structured file sorting


import os
import re
import ssort
from colorama import Fore

# get list of files in tests directory
files = os.listdir('tests/')
print(files)

test_cases = []

# find files of the form test[number].(json|yaml)
pattern = 'test[0-9]*.(json|yaml)'
input_files = [f for f in files if re.match(pattern, f)]
# for each input file find the sorting definition files of the form test[number].sort.(json|yaml)
# and the result files of the form test[number]-result.(json|yaml)
for input_file_path in input_files:
    test_number = int(input_file_path[4:-5])
    sorting_file_pattern = f'test{test_number}.sort.(json|yaml)'
    result_file_pattern = f'test{test_number}-result.(json|yaml)'
    sorting_files = [f for f in files if re.match(sorting_file_pattern, f)]
    result_files = [f for f in files if re.match(result_file_pattern, f)]
    test_cases.append({'input_file': input_file_path,
                      'sorting_files': sorting_files,
                       'result_file': result_files})

test_count = 0
tests_passed = 0
# run each test case
for test_case in test_cases:
    for sorting_file in test_case['sorting_files']:
        for result_file in test_case['result_file']:
            test_count += 1
            print(Fore.BLUE + 'Testing' + Fore.RESET + f' {test_case["input_file"]} with {sorting_file} and {result_file}')
            input_file_path = os.path.join('tests', test_case['input_file'])
            sorting_file_path = os.path.join('tests', sorting_file)
            result_file_path = os.path.join('tests', result_file)
            input_data = ssort.load_file(input_file_path)
            sorting_data = ssort.load_file(sorting_file_path)
            result_data = ssort.load_file(result_file_path)
            sorted_data = ssort.recursive_sort(input_data, sorting_data)

            if sorted_data != result_data:
                print(Fore.RED + "Test Failed")
                print(f'Sorted: {input_data}')
                print(f'Using: {sorting_data}')
                print(f'Expected: {result_data}')
                print(f'Got: {sorted_data}' + Fore.RESET)
            else:
                tests_passed += 1
                print(Fore.GREEN + 'Test passed'+Fore.RESET)

print(f'{tests_passed} of {test_count} tests passed')
