from . import arguments, arthashing, verification


def arthasher():
    args = arguments.arguments()
    if args.certificate:
        verification.verification(args)
    else:
        arthashing.arthashing(args)


if __name__ == '__main__':
    arthasher()
