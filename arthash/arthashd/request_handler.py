import datetime, os
from . import server
from .. util import check, hasher
from .. journals import keeper


class RequestHandler:
    def __init__(self, root, url_prefix, organization=None):
        self.record_hash = ''
        self.keeper = keeper.DictKeeper(root, organization)
        self.url_prefix = url_prefix

    def receive(self, message):
        original_keys = tuple(message)
        check.check_request(**message)

        message['timestamp'] = keeper.timestamp()

        message['record_hash'] = self.record_hash
        message['record_hash'] = hasher.record_hash(**message)

        self.keeper.add_record(message)
        journal_file = self.keeper.last
        message['urls'] = journal_file

        for k in original_keys:
            message.pop(k)

        return message
