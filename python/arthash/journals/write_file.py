def add_index_file(journal_file):
    pass


def _write_index_file(filename, body):
    with open(filename, 'w') as fp:
        fp.write(TEMPLATE.format(body=body))


TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>arthash</title>
</head>

<body>
{body}
</body> </html>
"""
