
import os, sys, re

DIRLIST=["BUILD","RPMS","SOURCES","SPECS","SRPMS"]
BUILDENVROOT="rpmbuild"

class RpmBuild( ):

    def __init__( self, projname, envpath=BUILDENVROOT ):
        self.__home = os.getenv( "HOME" )
        self.__envpath = envpath





    def __build_env( self ):

        fullenvpath = self.__home+"/"+self.__envpath
        for p in DIRLIST:
            if not os.path.exist( fullenvpath + "/" + p ):
                os.path.mkdir( fullenvpath + "/" + p )
