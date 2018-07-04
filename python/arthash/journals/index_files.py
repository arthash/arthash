import os

TD_TEMPLATE = '        <td><a href="{filename}"><pre>{root}</pre></a></td>'


def link_lines(directory):
    def linkable(f):
        if not f.startswith('.'):
            _, suffix = os.path.splitext(f)
            return suffix in ['', '.json']

    files = sorted(f for f in os.listdir(directory) if linkable(f))

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


def write_indexes(journal_file, levels):
    print('Created', journal_file)
    directory = journal_file
    for level in range(levels):
        title = TITLE % level
        directory = os.path.dirname(directory)
        body = '\n'.join(link_lines(directory))
        index_filename = os.path.join(directory, 'index.html')
        with open(index_filename, 'w') as fp:
            fp.write(DOC_TEMPLATE.format(**locals()))


TITLE = 'artHash index page level %d'

DOC_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>artHash index page {level}</title>
</head>
<body>
{body}
</body> </html>
"""
