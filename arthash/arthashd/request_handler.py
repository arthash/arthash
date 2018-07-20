import collections, datetime, os
from . import server
from .. util import check, hasher
from .. journals import keeper


class RecordKeeper(keeper.Keeper):
    def _get_record(self, data):
        return data

    def receive(self, message):
        record = collections.OrderedDict(sorted(message.items()))
        assert hasher.KEYS == tuple(record)
        self.add_record(record)

        return os.path.relpath(self.last, self.root)


class RequestHandler:
    def __init__(self, url_prefixes, root, organization=None):
        self.record_hash = ''
        self.url_prefixes = url_prefixes
        self.keeper = RecordKeeper(root, organization)

    def receive(self, message):
        check.check_request(**message)

        message['timestamp'] = keeper.timestamp()
        message['record_hash'] = self.record_hash

        self.record_hash = hasher.record_hash(**message)
        message['record_hash'] = self.record_hash

        url_base = self.keeper.receive(message)
        urls = [p + url_base for p in self.url_prefixes]

        return {
            'record_hash': message['record_hash'],
            'timestamp': message['timestamp'],
            'urls': urls,
        }
