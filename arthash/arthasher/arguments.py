import argparse, sys

from .. util import constants, files


def arguments(argv=sys.argv[1:]):
    parser = _make_parser()
    args = parser.parse_args(argv)
    _fix_document_and_certificate(args)
    return args


def _fix_document_and_certificate(args):
    # The user has no control over which way the documents come in in
    # drag-and-drop, so it might be that the document and certificate
    # need to be switched.
    cert, doc = args.certificate, args.document
    if not cert:
        return

    c, d = files.is_certificate(cert), files.is_certificate(doc)

    if c and d:
        raise ValueError('Both files are certificates')

    if not (c or d):
        raise ValueError('Neither file is a certificate')

    if not c:
        args.document, args.certificate = cert, doc


def _make_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'document', help='The document to arthash')

    parser.add_argument(
        'certificate', nargs='?', help='An optional arthash certificate',
        default=None)

    parser.add_argument(
        '-s', '--server', help='arthashd server address',
        default=constants.ADDRESS)

    parser.add_argument(
        '-p', '--port', help='arthashd server port ',
        default=constants.PORT)

    parser.add_argument(
        '-v', '--verbose', help='Print more messages',
        action='store_true')

    return parser
