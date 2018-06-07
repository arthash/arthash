import random


def distribution(data):
    # Do a statistical test with moderate bogosity.
    count = 16 * [0]
    for i in data:
        try:
            count[int(i, 16)] += 1
        except ValueError:
            raise ValueError('Not hex ' + data)
    return count


def random_hash():
    return ''.join(random.choice('0123456789abcdef') for s in range(64))


def dist():
    return distribution(random_hash())


def count_values_base(values, dist):
    return [sum((d == v) for d in dist) for v in values]


def count_values():
    d = dist()
    count = [sum(v == i for v in d) for i in range(16)]
    assert sum(count) == 16
    if count[15] or count[14] or count[13] or count[12] or count[11]:
        print(d, count)  # noqa T001
    return count


def count_many_values(repeats):
    counts = tuple(zip(*(count_values() for i in range(repeats))))
    return [max(*i) for i in counts]


def max_count_all_values(repeats):
    return [max(*zip(*i)) for i in range(repeats)]


def max_count_values(repeats, value):
    return max(*(count_values(value) for i in range(repeats)))
