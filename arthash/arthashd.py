import argparse, logging, sys, time
from daemon import runner, DaemonContext

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOGFILE = '/var/log/arthashd/arthashd.log',
DEFAULT_PIDFILE = '/var/run/arthashd/arthashd.pid',
COMMANDS = 'start', 'stop', 'restart'


class Runner(runner.DaemonRunner):
    # Fix error in runner.DaemonRunner's constructor.
    def __init__(self, app, action):
        self.action = action
        assert self.action in self.action_funcs
        self.app = app
        self.daemon_context = DaemonContext()
        self.daemon_context.pidfile = self.pidfile = runner.make_pidlockfile(
            app.pidfile_path, app.pidfile_timeout)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs=1, choices=COMMANDS)
    parser.add_argument('--logfile_path', '-l', default=DEFAULT_LOGFILE)
    parser.add_argument('--loglevel', '-v', default='INFO')
    parser.add_argument('--pidfile_path', '-p', default=DEFAULT_PIDFILE)
    parser.add_argument('--pidfile_timeout', '-t', default=5)

    return parser.parse_args(argv)


# http://www.gavinj.net/2012/06/building-python-daemon-process.html
class App:
    def __init__(self, command, logfile_path, pidfile_path,
                 pidfile_timeout, loglevel, log_name='arthashlog'):
        self.pidfile_path = pidfile_path
        self.pidfile_timeout = pidfile_timeout

        formatter = logging.Formatter(FORMAT)
        handler = logging.FileHandler(logfile_path)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(getattr(logging, loglevel))
        self.logger.addHandler(handler)

        self.runner = Runner(self, *command)
        # This ensures that the logger file handle does not get closed during
        # daemonization.
        self.runner.daemon_context.files_preserve = [handler.stream]

    def do_action(self):
        self.runner.do_action()

    def run(self):
        while True:
            logger.debug('Debug message')
            logger.info('Info message')
            logger.warn('Warning message')
            logger.error('Error message')
            time.sleep(10)


def main():
    args = vars(parse_args(sys.argv[1:]))
    app = App(**args)
    app.do_action()
