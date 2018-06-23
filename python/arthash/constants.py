DEBUG = True

FINAL_IP_ADDRESS = 'https://arthash.org'
DEBUG_IP_ADDRESS = 'http://localhost'
IP_ADDRESS = DEBUG_IP_ADDRESS if DEBUG else FINAL_IP_ADDRESS

PORT = 7887

PATH = ''

"""
The size of file chunks we read and hash.  The arthash computation is
independent of the CHUNKSIZE setting.
"""
CHUNKSIZE = 100000000
