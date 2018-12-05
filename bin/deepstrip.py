#!/usr/bin/env python3

import os,sys,re
import json
import subprocess, shlex

from pprint import pprint

def run( cmd, mode = {} ):

    result = list()
    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )

    prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE )
    for line in prc.stdout.readlines():
        result.append( line.lstrip().rstrip() )
    return result


def pkg_list( pkglist = list(), **opt ):
    res = list()

    for line in run( "yum list %s" % (" ".join(pkglist)) ):
        if re.match( "^Loading.+", line ): continue
        if re.match( "^Loaded.+", line ): continue
        if re.match( "^Installed Packages.*", line ): continue

        flds = re.split("\s+", line )
        if len( flds) == 3:
            pkgs = re.split("\.", flds[0] )
            item = {"package":pkgs[0], "arch":pkgs[1], "version":flds[1], "repo":flds[2], "installed":False }

            if re.match( "^@.+", flds[2] ):
                m = re.match( "@(.+)", flds[2])
                item['repo'] = m.group(1)
                item['installed'] = True

            res.append( item )

    return res

def unique_packages( pkglist ):
    res = dict()
    for i in pkglist:
        if i['package'] not in res:
            res[ i['package'] ] = 1

    return list( res.keys() )

def get_package_deps( pkg, **opt ):
    res = list()
    newest = ""
    dpath = "stage"

    if 'newest' in opt and opt['newest'] in (True, False) and opt['newest']: newest = "-n"
    if 'dpath' in opt: dpath = opt['dpath']

    if not os.path.exists( dpath ):
        os.makedirs( dpath )

    deps = run( "repotrack -t -p %s %s %s" % ( dpath, newest, pkg ))
    return [ os.path.basename( f ) for f in deps ]

def check_package_deps( pkg, **opt ):
    res = list()
    newest = ""

    if 'newest' in opt and opt['newest'] in (True, False) and opt['newest']: newest = "-n"

    deps = run( "repotrack -t -u %s %s" % ( newest, pkg ))
    return [ os.path.basename( f ) for f in deps ]


################################################################################
## Local file operaitons
################################################################################
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

def _read_text( filename ):
    result = list()
    try:
        fd = open( filename, "r" )
        for line in fd.readlines():
            result.append( line.lstrip().rstrip() )
        return result
    except Exception as e:
        print("ERROR Reading %s: %s" % ( filename, e ))

    return result

def _read_json( filename ):
    return json.loads( "\n".join( _read_text( filename ) ) )

def load_file( filename ):
    filesplit = re.split( r"\.", filename )
    if filesplit[-1] in ( "json" ):
        return _read_json( filename )
    else:
        return _read_text( filename )


def _write_json( filename, data ):
    return _write_text( filename, json.dumps( data, indent=2, sort_keys=True ) )

def _write_text( filename, data ):
    fd = open( filename, "w" )
    fd.write( str( data ) )
    fd.close()

def write_file( filename, data ):
    filesplit = re.split( "\.", filename )
    if filesplit[-1] in ( "json" ):
        return _write_json( filename, data )
    else:
        return _write_text( filename, data )

if __name__ == "__main__":
    opt = dict()
    opt['script'] = sys.argv.pop(0)
    opt['dpath'] = "stage"
    opt['ref'] = list()

    try:
        opt['mode'] = sys.argv.pop(0)
        if opt['mode'] not in ("check","download"):
            raise RuntimeError( "Bad mode")
    except Exception as e:
        print("ERROR: Need mode [check|download] <rfiles>")
        sys.exit(1)


    for f in sys.argv:
        opt['ref'] += load_file( f )

    allPackages = pkg_list( opt['ref'] )
    uniquePackages = unique_packages( allPackages )

    print("# Found %s packages" % ( len(allPackages)))
    print("# Found %s unique packages" % ( len( uniquePackages ) ))

    wantPackages = dict()
    wantFiles = dict()
    seenPackages = dict()
    for u in uniquePackages:
        print("# Checking package %s: %s / %s" % ( u, len( wantPackages.keys() ), len( uniquePackages ) ) )
        if opt['mode'] == "check":
            for d in check_package_deps( u, newest=True ):
                if d not in wantFiles: wantFiles[ d ] = 0
                if d not in wantPackages: wantPackages[ u ] = list()
                wantPackages[ u ].append( d )
                wantFiles[ d ] += 1

        elif opt['mode'] == "download":
            for d in  get_package_deps( u, newest=True, dpath=opt['dpath'] ):
                p = re.split("\s+", d )
                if p[1] not in wantFiles: wantFiles[ p[1] ] = 0
                if p[1] not in wantPackages: wantPackages[ u ] = list()
                wantPackages[ u ].append( p[1] )
                wantFiles[ p[1] ] += 1

    print("# Want %s packages" % ( len(list( wantFiles.keys() )) ) )
    print( "\n".join( sorted( list( wantFiles.keys() ) ) ) )
