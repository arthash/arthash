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
