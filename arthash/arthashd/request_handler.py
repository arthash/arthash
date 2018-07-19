import datetime, flask, os
from . import server
from .. util import check, hasher


class RequestHandler:
    def __init__(self):
        self.record_hash = None
        self.keeper = None

    def receive(self, art_hash, public_key, signature):
        check.SHA256(art_hash)
        check.RSAPublicKey(public_key)
        check.RSASignature(signature)

        timestamp = _timestamp()
        self.keeper.update(timestamp)


def _timestamp():
    return datetime.datetime.utcnow().isoformat()
