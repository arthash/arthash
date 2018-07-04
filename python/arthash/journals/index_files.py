import os

TD_TEMPLATE = '        <td><a href="{filename}"><pre>{root}</pre></a></td>'


def link_lines(directory):
    files = sorted(f for f in os.listdir(directory) if not f.startswith('.'))

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
    print('Created', journal_file)
    directory = journal_file
    for title in TITLES:
        directory = os.path.dirname(directory)
        body = '\n'.join(link_lines(directory))
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
