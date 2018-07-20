from . import arguments, arthashing, verification


def arthasher():
    args = arguments.arguments()
    if args.certificate:
        verification.verification(args.document, args.certificate)
    else:
        arthashing.arthashing(args.document, args.server, args.port)


if __name__ == '__main__':
    arthasher()
