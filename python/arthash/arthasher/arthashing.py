import os, webbrowser
from .. import files
from .. util import data_file, public_private_key


def arthashing(args):
    arthash = files.hash_file(args.document)

    public, private = public_private_key.public_private_key()

    url = '%s:%s/put/%s' % (args.server, args.port, arthash)
    data = data_file.get(url)

    d = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    d = os.path.join(d, 'html', 'certificate-generator.html')
    d = os.path.abspath(d)
    url = 'file:///%s?' % data

    webbrowser.open(url, new=0, autoraise=True)
