#! /usr/bin/env python3

import inspect
import os
import requests
from typing import List, Optional


COOKIES = {'session':'53616c7465645f5f956c24443fdf0814a6393b3a8d6839acddca34c7175179eeba3c432c44be640c125d51f28e7a1e93'}

def _main_module_name():
    # This will return a list of frame records, 
    # [-1] is the first frame.
    frame_records = inspect.stack()[-1]
    # Index 1 of frame_records is the full path of the module,
    # we can then use inspect.getmodulename() to get the
    # module name from this path.
    module = inspect.getmodulename(frame_records[1])
    return module


def _get_default_file_name() -> str:
    return os.path.join('input', _main_module_name() + '.txt')


def _load_cache(filename: str) -> Optional[str]:
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read().rstrip()
    return None


def _save_cache(filename: str, data: str) -> None:
    with open(filename, 'w') as f:
        f.write(data)


def _read_from_web(filename: str) -> str:
    day_nr = int(os.path.splitext(filename)[0][-2:])
    url = f'https://adventofcode.com/2020/day/{day_nr}/input'
    #Request.add_header('Cookie', 'session=36f84923bc7144dfb56214fc3efde78b...')    
    response = requests.get(url, cookies=COOKIES)
    response.raise_for_status()
    return response.text


def get_raw_input(filename: str = None):
    if filename:
        with open(filename) as f:
            return f.read().rstrip()

    filename = _get_default_file_name()
    if not (data := _load_cache(filename)):
        data = _read_from_web(filename)
        _save_cache(filename, data)
    return data


def get_file_lines(filename: str = None) -> List[str]:
    lines = get_raw_input(filename).split('\n')
    if len(lines[-1].rstrip()) == 0:
        lines.pop()
    return lines