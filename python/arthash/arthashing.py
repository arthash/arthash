from . import files


def arthashing(args):
    arthash = files.hash_file(args.document)
    return arthash
