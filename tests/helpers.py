import sys
def is_str(target_str):
    if sys.version_info[0] >= 3:
        return isinstance(target_str, str) 
    return isinstance(target_str, basestring)
    