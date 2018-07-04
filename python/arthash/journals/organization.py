import math, os


class Organization:
    """
    How the JSON files are organized on disk.  This is an immutable class.
    """
    def __init__(self, page_size=256, levels=4):
        self.page_size = page_size
        self.levels = levels
        self.digit_size = math.ceil(math.log2(page_size) / 4)
        self.digit_format = '%0' + str(self.digit_size) + 'x'

    def next_file(self, filename):
        segments = []
        for f in range(self.levels):
            filename, d = os.path.split(filename)
            segments.insert(0, d)

        root, suffix = os.path.splitext(segments[-1])
        if suffix != '.json':
            raise ValueError(suffix)
        segments[-1] = root

        numbers = [int(i, 16) for i in segments]

        for i in reversed(range(self.levels)):
            numbers[i] += 1
            if numbers[i] < self.page_size:
                break
            if i:
                numbers[i] = 0

        parts = [self.digit_format % i for i in numbers]
        parts[-1] += suffix
        filename and parts.insert(0, filename)
        return os.path.join(*parts)
