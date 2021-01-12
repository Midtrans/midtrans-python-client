import sys

_PYTHON_VERSION = sys.version_info[:2]

def merge_two_dicts_shallow(x, y):
    """
    Given two dictionaries, merge them into a new dict as a shallow copy.
    merging two dict that support Python 2 according https://stackoverflow.com/a/26853961/2212582
    unfortunately the fastest `**` unpack method will result in syntax error on Python 2
    """
    z = x.copy()
    z.update(y)
    return z