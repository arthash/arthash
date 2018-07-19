import logging, os, requests, webbrowser
from .. util import constants, crypto, files

log = logging.getLogger(__name__)
RESULT_KEYS = set(('timestamp', 'record_hash', 'journal'))


def arthashing(args):
    art_hash = files.hash_document(args.document)
    private_key = crypto.make_private_key()
    signature = crypto.sign(private_key, art_hash)
    public_key = crypto.public_key_string(private_key)

    data = {
        'art_hash': art_hash,
        'public_key': public_key,
        'signature': signature.hex(),
    }
    url = '%s:%s%s' % (args.server, args.port, constants.PUT_URL)
    if True:
        import json
        print(json.dumps(data, indent=4))
        print(url)
        return
    response = requests.put(url, data=data).json()

    if set(response) != RESULT_KEYS:
        raise ValueError('Do not understand keys in ' + str(response))

    response['private_key'] = crypto.private_key_string(private_key)

    if True:
        import json
        print(json.dumps(response, indent=4))
        return

    d = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    d = os.path.join(d, 'html', 'certificate-generator.html')
    d = os.path.abspath(d)
    url = 'file:///%s?' % data

    webbrowser.open(url, new=0, autoraise=True)
