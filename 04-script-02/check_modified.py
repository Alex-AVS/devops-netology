#!/usr/bin/env python3

import os
import sys
import subprocess
import re

try:
    path = sys.argv[1]
except IndexError:
    print("Укажите путь к репозиторию.")
    exit()

expanded_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

try:
    result_os = subprocess.run(["git", "status", "-s"], cwd=expanded_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
except (FileNotFoundError, NotADirectoryError):
    print(
        f'Путь {expanded_path} не найден'
    )
    exit()

if result_os.find('fatal:') >= 0:
    print(
        f'В папке {expanded_path} репозиторий git не найден.')
    exit()

mod_types = {"A\s": "new", "\sM": "modified", "AM": "modified new", "\sD": "deleted", "R\s": "renamed", "\?\?": "untracked"}

for result in result_os.split("\n"):
     for key in mod_types.keys():
        regexp = re.compile(r"^" + key + "\s*")
        if regexp.search(result):
            prepare_result = re.sub(regexp, '', result).split(' -> ')

            if mod_types[key] == 'renamed':
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[1])} <- {prepare_result[0]}')
            else:
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[0])}')

