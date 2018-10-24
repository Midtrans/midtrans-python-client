import sys
def is_str(target_str):
    if sys.version_info[0] >= 3:
        return type(target_str) is str 
    return target_str is basestring
    