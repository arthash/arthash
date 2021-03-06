"""

Detect malformed hashes.
Attempt to detect spam hashes.

"""

import collections, math, hashlib


def entropy(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    key_dict = dict.fromkeys(list(string))
    prob = [string.count(c) / len(string) for c in key_dict]

    # calculate the entropy
    return -sum(p * math.log(p) / math.log(2) for p in prob)


def entropy_ideal(length):
    "Calculates the ideal Shannon entropy of a string with given length"

    prob = 1.0 / length
    return -1.0 * length * prob * math.log(prob) / math.log(2.0)


def entropy_hashes(count, value=b'x'):
    # 100000: (3.411598784883635, 3.977217001462483)
    # 1000000: (3.326479333192638, 3.9829127510968623)
    h = hashlib.sha256()
    min_entropy = 10000000000
    max_entropy = -1

    for i in range(count):
        e = entropy(h.hexdigest())
        min_entropy = min(e, min_entropy)
        max_entropy = max(e, max_entropy)
        h.update(value)
    return min_entropy, max_entropy


def generate_hashes(count, value=b'x'):
    h = hashlib.sha256()

    min_count = 65
    max_count = -1

    for i in range(count):
        for k, v in collections.Counter(h.hexdigest()).items():
            min_count = min(min_count, v)
            max_count = max(max_count, v)
        h.update(value)

    return min_count, max_count
