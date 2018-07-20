import datetime, flask, os
from . import server
from .. util import check, hasher
from .. journals import keeper


class RequestHandler:
    def __init__(self, root, organization=None):
        self.record_hash = None
        self.keeper = keeper.DictKeeper(root, organization)

    def receive(self, message):
        original_keys = tuple(message)
        check.check_request(**message)

        message['timestamp'] = keeper.timestamp()
        message['record_hash'] = hasher.record_hash(**message)

        self.keeper.add_record(message)
        message['urls'] = self.keeper.last

        for k in original_keys:
            message.pop(k)

        return flask.jsonify(message)
