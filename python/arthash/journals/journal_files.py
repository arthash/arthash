import json, os
from os import listdir, makedirs

open = __builtins__['open']


def write(journal_file, page):
    exists = os.path.exists(journal_file)
    if not exists:
        makedirs(os.path.dirname(journal_file), exist_ok=True)

    with open(journal_file, 'w') as fp:
        json.dump(page, fp, indent=2)

    if False and not exists:
        write_indexes(journal_file)


def read(journal_file):
    return json.load(open(journal_file))


def link_lines(directory):
    files = sorted(f for f in listdir(directory) if not f.startswith('.'))

    yield '<table>'
    for i, filename in enumerate(files):
        if i == 0:
            yield '    <tr>'
        elif i % 16 == 0:
            yield '    </tr>'
            yield '    <tr>'
        root, suffix = os.path.splitext(filename)
        if not suffix:
            filename += '/index.html'
        yield TD_TEMPLATE.format(filename=filename, root=root)

    yield '    </tr>'
    yield '</table>'


def write_indexes(journal_file):
    d = os.path.dirname(journal_file)
    write_index(d)
    write_index(os.path.dirname(d))
    write_index(os.path.dirname(os.path.dirname(d)))
    write_index(os.path.dirname(os.path.dirname(os.path.dirname(d))))


def write_index(directory, title='artHash index page'):
    body = '\n'.join(link_lines(directory))
    index_filename = os.path.join(directory, 'index.html')
    with open(index_filename, 'w') as fp:
        fp.write(DOC_TEMPLATE.format(title=title, body=body))


TD_TEMPLATE = '        <td><a href="{filename}"><pre>{root}</pre></a></td>'

DOC_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>{title}</title>
</head>
<body>
{body}
</body> </html>
"""
