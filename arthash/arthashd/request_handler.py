import collections, datetime, os
from . import server
from .. journals import keeper
from .. util import check, hasher


class RequestHandler:
    def __init__(self, url_prefixes, root, organization=None):
        self.keeper = keeper.Keeper(root, organization)
        self.url_prefixes = url_prefixes

    def receive(self, art_hash, public_key, signature):
        check.SHA256(art_hash)
        check.RSAPublicKey(public_key)
        check.RSASignature(signature)

        timestamp = keeper.timestamp()
        if self.keeper.page:
            old_record_hash = self.keeper.page[-1]['record_hash']
        else:
            old_record_hash = ''

        new_record_hash = hasher.record_hash(
            art_hash=art_hash,
            record_hash=old_record_hash,
            signature=signature,
            timestamp=timestamp)

        self.keeper.add_record(
            art_hash=art_hash,
            record_hash=new_record_hash,
            signature=signature,
            timestamp=timestamp)

        url = self.keeper.url()
        urls = [p + url for p in self.url_prefixes]

        return {
            'record_hash': new_record_hash,
            'timestamp': timestamp,
            'urls': urls,
        }
