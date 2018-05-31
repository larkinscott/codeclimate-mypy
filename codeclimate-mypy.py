#!/usr/bin/env python3

import glob
import json
import re
import os
import sys
from mypy import api

line_number_regex = ":(\d+):"
file_name_regex = "^(.+?):"
issue_description_error_regex = "error(.*)"
issue_description_note_regex = "note(.*)"
# need to add this regex in
issue_description_warning_regex = "warning(.*)"

try:
    with open('/config.json') as config_file:
        config = json.loads(config_file.read())
except IOError:
    config = {}

include_paths = config.get('include_paths', ['./'])
exclude_paths = config.get('exclude_paths', [])
options = config.get('options', [])

def file_path() -> list:
    python_files = []

    for path in include_paths:
        if path.endswith('.py'):
            python_files.append(path)
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.py'):
                    python_files.append(os.path.join(dirname, filename))

    for path in exclude_paths:
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.py'):
                    python_files.remove(os.path.join(dirname, filename))

    for option in options:
        python_files.insert(0, option)

    return(python_files)

def analyze(python_files: list) -> str:
    mypy_output = api.run(python_files)

    if mypy_output[0]:
        successful_results = mypy_output[0]

        split_issues_on_newline = successful_results.split('\n')
        del split_issues_on_newline[-1]

        for issue in split_issues_on_newline:
            line_number = re.search(line_number_regex, issue)
            if line_number is not None:
                line_number = line_number.group(1)
            else:
                line_number = 1

            file_name = re.search(file_name_regex, issue).group(1)

            issue_description = re.search(issue_description_error_regex, issue)
            if issue_description is not None:
                issue_description = issue_description.group(1)
            elif issue_description is None:
                issue_description = re.search(issue_description_note_regex, issue).group(1)
            else:
                issue_description = re.search(issue_description_warning_regex, issue).group(1)

            codeclimate_json = dict()
            codeclimate_json['type'] = 'issue'
            codeclimate_json['check_name'] = 'Static Type Check'
            codeclimate_json['categories'] = ['Style']

            codeclimate_json['description'] = issue_description

            location = dict()
            location['path'] = file_name
            location['positions'] = {
                'begin': {
                    'line': int(line_number),
                    'column': 0,
                },
                'end': {
                    'line': int(line_number),
                    'column': 0,
                },
            }

            codeclimate_json['location'] = location
            codeclimate_json['severity'] = 'info'

            codeclimate_json_string = json.dumps(codeclimate_json, indent=4)
            print(codeclimate_json_string + "\0")

    if mypy_output[1]:
        unsuccessful_result = mypy_output[1]

        print(unsuccessful_result, file=sys.stdout)

python_files = file_path()

if len(python_files) == 0:
    quit()
else:
    analyze(python_files)
