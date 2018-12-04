#!/usr/bin/python

import os, re, sys
import multiprocessing
import subprocess, shlex

from pprint import pprint

## =============================================================
## Constants
## =============================================================

## =============================================================
## QUEUEs
## =============================================================

## =============================================================
## utils
## =============================================================
def dirtree( path, rx=r".*" ):
    result = list()
    for f in os.listdir( path ):
        p = "%s/%s" % ( path, f )
        if os.path.isdir( p ):
            result += dirtree( p, rx )
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



def version_dep( dps ):
    dps_parts = re.split( r"\s+", dps )
    if len( dps_parts ) == 3:
        return dps_parts[-1]
    return None

def dependency_split( dps ):
    return re.split( r"\s+", dps )

def dependency_valid( dps_list, dps_check ):

    chk_dep = dependency_split( dps_check )
    for dps_ref in dps_list:
        ref_dep = dependency_split( dps_ref )

        ## check if dep name is same in both
        ##      if is, check version if available
        ##      else if version not available, return True
        ##      else, continue searching

## =============================================================
## processes
## =============================================================
def exec_command( cmd, mode = {} ):

    result = list()
    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )

    prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE )
    for line in prc.stdout.readlines():
        result.append( line.lstrip().rstrip() )
    return result

def load_rpm_info( filename, fields=["Name","Version","Release","Architecture"] ):

    if not file_is_type( filename, "rpm" ):
        raise AttributeError("Wrong file type for %s" % ( filename ) )

    result = dict()
    for line in exec_command( "rpm -qip --nosignature %s" % ( filename ) ):
        line_split = re.split( r":", line )
        if len( line_split ) < 2:
            continue

        lk = line_split[0].lstrip().rstrip()
        lv = line_split[1].lstrip().rstrip()

        for f in fields:
            if f == lk: result[ f.lower() ] = lv

    return result


def load_rpm_dep( filename ):

    if not file_is_type( filename, "rpm" ):
        raise AttributeError("Wrong file type for %s" % ( filename ) )

    result = load_rpm_info( filename )
    result['files'] = list()
    result['requires'] = list()
    result['provides'] = list()

    for f in exec_command( "rpm -q -p --nosignature --list %s" % ( filename ) ):
        if f not in result['files']: result['files'].append( f )

    for r in exec_command( "rpm -q --nosignature -p --requires %s" % ( filename ) ):
        if r not in  r: result['requires'].append( r )

    for p in exec_command( "rpm -q --nosignature -p --provides %s" % ( filename ) ):
        if p not in result['provides']: result['provides'].append( p )

    return result

## =============================================================
## =============================================================
def print_help( scr ):
    print("%s <path>" % ( scr ) )

if __name__ == "__main__":

    config = dict()
    config['debug'] = True
    config['help'] = False

    config['script'] = sys.argv.pop(0)

    try:
        config['path'] = sys.argv.pop(0)
    except Exception as e:
        print_help( config['script'] )
        sys.exit(1)

    fcache = dict()
    dep_cache = dict()
    prv_cache = dict()

    filelist = dirtree( config['path'], r"\.rpm$")
    filelist_len = len( filelist )

    for i, f in enumerate( filelist ):
        fcache[ f ] = load_rpm_dep( f )
        v = fcache[ f ]['version']
        r = fcache[ f ]['release']
        ff = len( fcache[ f ]['files'] )
        fr = len( fcache[ f ]['requires'] )
        fp = len( fcache[ f ]['provides'] )
        print("# INFO: Loaded %s/%s %s with \t [%s.%s] \t %s / %s / %s" % ( i+1, filelist_len, f, v,r, ff, fr, fp ) )

    for f in fcache:
        for x in fcache[ f ]['provides']:
            mod = dependency_split( x )[0]
            if mod not in dep_cache:
                dep_cache[ mod ] = filename( f )

    print("# INFO: Dependency cache %s" % (len( dep_cache)) )
#    pprint( dep_cache )
#    pprint( fcache )

elif __name__ == "rpmdepcheck":
    import unittest
