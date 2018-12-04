#

import sys, os, re
import subprocess, shlex


class BaseCommand( object ):

    def __init__(self):
        pass

    def run( self, cmd, mode = {} ):

        result = list()
        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE )
        for line in prc.stdout.readlines():
            result.append( line.lstrip().rstrip() )
        return result




class RpmCommand( BaseCommand ):

    def __init__(self):
        pass

class YumCommand( BaseCommand ):

    def __init__(self):
        pass

class CreateRepoCommand( BaseCommand ):

    def __init__(self):
        pass
