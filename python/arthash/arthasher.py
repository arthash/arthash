import json, requests
from . import arguments, hasher, constants, files


def make_hash(document):
    return hasher.hasher(document, constants.CHUNKSIZE)


def verification(document, certificate):
    """
    Returns the timestamp when the arthash in the certificate was journaled.

    Raises a ValueError if the certificate is malformed, if there is no journal
    page or it is inaccessible, or if the journal page does not include
    the arthash.
    """
    certificate_data = json.load(open(certificate))

    try:
        arthash = certificate_data['arthash']
        journal_url = certificate_data['journal_url']
    except KeyError as e:
        raise ValueError('No "%s" in certificate %s' % (e.args[0], certificate))

    arthash_actual = make_hash(document)
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


def arthashing(document):
    arthash = make_hash(document)
    # TODO
    return arthash


def arthasher():
    arguments.run(arthashing, verification)


if __name__ == '__main__':
    arthasher()
