import os, webbrowser
from . import data_file, files


def arthashing(args):
    arthash = files.hash_file(args.document)
    url = '%s:%s/put/%s' % (args.server, args.port, arthash)
    data = data_file.get(url)

    d = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    d = os.path.join(d, 'html', 'certificate-generator.html')
    d = os.path.abspath(d)
    url = 'file:///%s?' % data

    webbrowser.open(url, new=0, autoraise=True)
