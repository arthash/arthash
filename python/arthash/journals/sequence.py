import os
from os import listdir
from os.path import isdir
from .. util import files


def last_file(f):
    while isdir(f):
        dfiles = [f for f in listdir(f) if files.is_journal_file(f)]
        if not dfiles:
            return
        f = os.path.join(f, sorted(dfiles)[-1])
    return f


def next_file(f):
    f, d4_json = os.path.split(f)
    f, d3 = os.path.split(f)
    f, d2 = os.path.split(f)
    f, d1 = os.path.split(f)
    if f:
        raise ValueError(f)

    d4, suffix = os.path.splitext(d4_json)
    if suffix != '.json':
        raise ValueError(suffix)

    numbers = [int(i, 16) for i in (d1, d2, d3, d4)]

    for i in reversed(range(4)):
        numbers[i] += 1
        if numbers[i] <= 255:
            break
        if i:
            numbers[i] = 0

    parts = ['%02x' % i for i in numbers]
    parts[-1] += suffix
    return os.path.join(*parts)
