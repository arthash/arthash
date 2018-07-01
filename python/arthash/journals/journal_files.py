import json, os
from . import link_lines


def write(journal_file, page):
    exists = os.path.exists(journal_file)
    if not exists:
        os.makedirs(os.path.dirname(journal_file), exist_ok=True)

    with open(journal_file, 'w') as fp:
        json.dump(page, fp, indent=2)

    if False and not exists:
        write_indexes(journal_file)


def read(journal_file):
    return json.load(open(journal_file))


def write_indexes(journal_file):
    d = os.path.dirname(journal_file)
    write_index(d)
    write_index(os.path.dirname(d))
    write_index(os.path.dirname(os.path.dirname(d)))
    write_index(os.path.dirname(os.path.dirname(os.path.dirname(d))))


def write_index(directory, title='artHash index page'):
    body = '\n'.join(link_lines.link_lines(directory))
    index_filename = os.path.join(directory, 'index.html')
    with open(index_filename, 'w') as fp:
        fp.write(DOC_TEMPLATE.format(title=title, body=body))


DOC_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>{title}</title>
</head>
<body>
{body}
</body> </html>
"""
