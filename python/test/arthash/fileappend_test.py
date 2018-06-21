from arthash import fileappend

import threading, time, sys


class FileLocker(threading.Thread):
    def __init__(self, filename, seconds, **kwds):
        super(FileLocker, self).__init__(**kwds)
        self.filename = filename
        self.seconds = seconds

    def run(self):
        with fileappend.locked_append(self.filename):
            time.sleep(self.seconds)


if __name__ == '__main__':
    filename = sys.argv[1]
    FileLocker(filename, 2).start()
    time.sleep(0.1)
    with fileappend.locked_append(filename) as fd:
        print(type(fd))  # noqa T001
        fd.write(b'made it!\n')
