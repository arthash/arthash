import argparse, sys

from . import constants, files


def run(arthashing, verification, argv=sys.argv):
    """
    Arguments:
      arthashing: a function (document, args)
      verification: a function (document, certificate, args)
    """
    args = _make_parser().parse(argv)
    cert, doc = args.certificate, args.document

    if not cert:
        return arthashing(doc, args)

    c, d = files.is_certificate(cert), files.is_certificate(doc)

    if c and d:
        raise ValueError('Both files are certificates')

    if not (c or d):
        raise ValueError('Neither file is a certificate')

    if not c:
        # doc is a certificate, and cert isn't.
        doc, cert = cert, doc

    return verification(doc, cert, args)


def _make_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'document', nargs='1', help='The document to arthash')

    parser.add_argument(
        'certificate', nargs='+', help='An optional arthash certificate',
        default=None)

    parser.add_argument(
        '-i', '--ipaddress', help='arthashd server IP address',
        default=constants.IP_ADDRESS)

    parser.add_argument(
        '-p', '--port', help='arthashd server port ',
        default=constants.PORT)

    parser.add_argument(
        '-v', '--verbose', help='Print more messages',
        action='store_true')

    return parser
