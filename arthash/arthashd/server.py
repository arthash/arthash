import flask, http.client

from werkzeug.serving import run_simple
from werkzeug.datastructures import ImmutableOrderedMultiDict

NAME = 'arthashd'


class Server:
    def __init__(self, port, external_access, handler=None, **kwds):
        self.handler = handler
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.server.route('/', methods=['PUT'])(self.put)
        self.server.route('/', methods=['GET'])(self.get)

    def get(self):
        return 'ok'

    def put(self):
        try:
            self.handler(**flask.request.values)
        except:
            flask.abort(http.client.BAD_REQUEST)

    def run(self):
        run_simple(self.hostname, self.port, self.app, threaded=True)
