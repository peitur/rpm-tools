#

import os
import json, yaml
import datetime, time
from pprint import pprint

def temp_dir( ):
    pass

def file_stat( filename ):
    pass

def read_dir( path, rx=r".*" ):
    pass

def read_tree( path, rx=r".*" ):
    result = list()
    for f in os.listdir( path ):
        p = "%s/%s" % ( path, f )
        if os.path.isdir( p ):
            result += read_tree( p, rx )
        else:
            if re.search( rx, f ):
                result.append( p )
    return result

def filename( filename ):
    return re.split( r"/", filename )[-1]

def filetype( filename ):
    return re.split( r"\.", filename )[-1]

def file_is_type( filename, tp ):
    chkt = filetype( filename )
    if chkt == tp:
        return True
    return False


def read_file( filename, format_handler=None ):
    pass

def write_file( filename, data, format_handler=None )
    pass
