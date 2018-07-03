import json, os
from . import link_lines


def write(journal_file, page):
    exists = os.path.exists(journal_file)
    if not exists:
        os.makedirs(os.path.dirname(journal_file), exist_ok=True)

    with open(journal_file, 'w') as fp:
        json.dump(page, fp, indent=2)

    if not exists:
        _write_indexes(journal_file)


def read(journal_file):
    return json.load(open(journal_file))


def _write_indexes(journal_file):
    print('Created', journal_file)
    directory = journal_file
    for title in TITLES:
        directory = os.path.dirname(directory)
        body = '\n'.join(link_lines.link_lines(directory))
        index_filename = os.path.join(directory, 'index.html')
        with open(index_filename, 'w') as fp:
            fp.write(DOC_TEMPLATE.format(title=title, body=body))


TITLES = (
    'artHash index page level 0',
    'artHash index page level 1',
    'artHash index page level 2',
    'artHash index page level 3',
)

DOC_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>{title}</title>
</head>
<body>
{body}
</body> </html>
"""
