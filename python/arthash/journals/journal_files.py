import json, os
from . import index_files


def write(journal_file, page):
    exists = os.path.exists(journal_file)
    if not exists:
        os.makedirs(os.path.dirname(journal_file), exist_ok=True)

    with open(journal_file, 'w') as fp:
        json.dump(page, fp, indent=2)

    if not exists:
        index_files.write_indexes(journal_file)


def read(journal_file):
    return json.load(open(journal_file))
