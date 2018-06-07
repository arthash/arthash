#!/usr/bin/env python3

# import cgitb
# cgitb.enable()

from arthash import fileappend
from arthash.experimental import hash_distributions

HEADER = """Content-Type: text/plain
"""

def run_cgi(filename, hash_code):
    print(HEADER)

    try:
        fileappend.append_hash(filename, hash_code)

    except Exception as e:
        print('ERROR:', e, 'for hash', '"%s"' % hash_code)
        raise
    else:
        print('SUCCESS:', hash_code)


if __name__ == '__main__':
    import sys

    # When called from CGI, the filename is a fixed constant.
    try:
        filename = sys.argv[1]
    except:
        filename = '/tmp/arthashlist.txt'

    # When called from CGI, the sha256_hash is a field from the form.
    try:
        sha256_hash = sys.argv[2]
    except:
        sha256_hash = hash_distributions.random_hash()

    run_cgi(filename, sha256_hash)
