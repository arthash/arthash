SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]


def is_certificate(file):
    return any(file.endswith(s) for s in CERT_SUFFIXES)
