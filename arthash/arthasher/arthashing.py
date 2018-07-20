import json, logging, os, requests, webbrowser
from .. util import constants, crypto, files

log = logging.getLogger(__name__)
RESPONSE_KEYS = set(('timestamp', 'record_hash', 'journal_urls'))


def signed_hash(document):
    private_key = crypto.make_private_key()
    public_key = private_key.public_key()
    art_hash = files.hash_document(document)
    data = {
        'art_hash': art_hash,
        'signature': crypto.sign(private_key, art_hash),
        'public_key': crypto.public_key_to_string(public_key),
    }
    return private_key, data


def distribute_to_server(args, data):
    url = '%s:%s%s' % (args.server, args.port, constants.PUT_URL)
    response = requests.put(url, data=data).json()

    if set(response) != RESPONSE_KEYS:
        raise ValueError('Do not understand keys in ' + str(response))

    return response


def generate_certificate(filename, data):
    d = os.path.dirname(os.path.dirname(os.path.dirname(filename)))
    d = os.path.join(d, 'html', 'certificate-generator.html')
    d = os.path.abspath(d)
    url = 'file:///%s?' % data

    webbrowser.open(url, new=0, autoraise=True)


def write_data(data):
    print(json.dumps(data, indent=2))


def arthashing(args):
    private_key, data = signed_hash(args.document)
    response = data or distribute_to_server(args, data)

    pks = crypto.private_key_to_string(private_key)
    data = dict(response, private_key=pks)
    write_data(data)
