import flask, os
from werkzeug.serving import run_simple


class RestServer(runnable.LoopThread):
    def __init__(self, port, external_access, directory):
        super().__init__()
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.app = flask.Flask(__name__)
        self.app.route('/post/<address>')(self.post)

    def run(self):
        run_simple(self.hostname, self.port, self.app, threaded=True)
