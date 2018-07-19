DEBUG = True

FINAL_ADDRESS = 'https://arthash.org'
DEBUG_ADDRESS = 'http://localhost'
ADDRESS = DEBUG_ADDRESS if DEBUG else FINAL_ADDRESS

PORT = 7887
PUT_URL = '/put'
JOURNAL_PATH = 'journal'

"""
The size of file chunks we read and hash.  The arthash computation is
independent of the CHUNKSIZE setting.
"""
CHUNKSIZE = 100000000
