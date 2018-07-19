import json, requests
from .. util import data_file, files
from . import arguments


def verification(document, certificate, args):
    """
    Returns the timestamp when the arthash in the certificate was journaled.

    Raises a ValueError if the certificate is malformed, if there is no journal
    page or it is inaccessible, or if the journal page does not include
    the arthash.
    """
    try:
        certificate_data = data_file.get(certificate)
    except:
        raise ValueError("Can't read certificate " + certificate)

    try:
        arthash = certificate_data['arthash']
        journal_url = certificate_data['journal_url']
    except KeyError as e:
        raise ValueError('No "%s" in certificate %s' % (e.args[0], certificate))

    arthash_actual = files.hash_document(document)
    if arthash_actual != arthash:
        raise ValueError('arthashes do not match')

    try:
        journal = json.loads(requests.get(journal_url).text)
    except:
        raise ValueError('Error reading journal ' + journal_url)

    hashes, timestamps = zip(*journal)
    try:
        i = hashes.index(arthash)
    except ValueError:
        raise ValueError('Arthash "%s" was not in journal %s' % (
            arthash, journal_url))

    return timestamps[i]
