import datetime, flask, os
from . import server
from .. util import check, hasher
from .. journals import keeper


class RequestHandler:
    def __init__(self, root, organization=None):
        self.record_hash = None
        self.keeper = keeper.DictKeeper(root, organization)

    def receive(self, art_hash, public_key, signature):
        check.SHA256(art_hash)
        check.RSAPublicKey(public_key)
        check.RSASignature(signature)
        timestamp = keeper.timestamp()

        record_hash = None
        record = {
            'art_hash': art_hash,
            'public_key': public_key,
            'record_hash': record_hash,
            'signature': signature,
            'timestamp': timestamp,
        }

        self.keeper.add_record(record)
