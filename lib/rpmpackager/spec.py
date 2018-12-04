
import os, sys, re

from pprint import pprint

PREAMBLE={
    "name": { "title": "Name" , "mandatory": True },
    "version": { "title": "Version", "default":"0.0.0", "mandatory": True },
    "release": { "title": "Release", "default":'%{?dist}' , "mandatory": True},
    "summary": { "title": "Summary", "mandatory": True },
    "license": { "title": "License", "mandatory": True, "default":"Apache" },
    "url": { "title": "URL", "mandatory": False },
    "source": { "title": "Source", "iteration": True, "low" : 0, "high": 3 , "default":[], "mandatory": True },
    "patch": { "title": "Patch", "iteration": True, "low": 0, "high": 45 , "default":[], "mandatory": False },
    "buildarch": { "title": "BuildArch", "default":"x86_64" , "mandatory": False },
    "buildrequires": { "title": "BuildRequires", "mandatory": False },
    "buildroot": { "title": "BuildRoot", "default":'%{_buildroot}/%{name}-root' },
    "requires": { "title": "Requires" , "mandatory": False },
    "excludearch": { "title": "ExcludeArch", "mandatory": False }
}

DIRECTIVES={
    "description":'%description',
    "prep":'%prep',
    "build":'%build',
    "install":'%install',
    "check":'%check',
    "files":'%files',
    "changelog":'%changelog'
}
## lazy way of ordering ...
DIRECTIVES_ORDER=["description","prep","build","install","check","files","changelog"]

SEL_MACROS={

}


CONSTANTS={
    "rpmbuildroot":'${RPM_BUILD_ROOT}',
    "rpmsourcedir":'${RPM_SOURCE_DIR}',
    "rpmbuilddir":'${RPM_BUILD_DIR}',
    "rpmoptflags":'${RPM_OPT_FLAGS}',
    "rpmldflags":'${RPM_LD_FLAGS}',
    "rpmarch":'${RPM_ARCH}',
    "rpmos":'${RPM_OS}',
    "rpmdocdir":'${RPM_DOC_DIR}',
    "rpmpackagename":'${RPM_PACKAGE_NAME}',
    "rpmpackageversion":'${RPM_PACKAGE_VERSION}',
    "rpmpackagerelease":'${RPM_PACKAGE_RELEASE}',
    "rpmbuildncpus":'${RPM_BUILD_NCPUS}'
}




##==============================================================================
##
##
##
##==============================================================================
class RpmSpecPreamble( ):
    def __init__( self ):
        self.__prm_data = {}
        for prm in PREAMBLE:
            if "default" in PREAMBLE[ prm ]:
                self.__prm_data[ prm ] = PREAMBLE[ prm ]["default"]


    def set( self, key, val ):
        if key not in PREAMBLE:
            raise AttributeError( "Invalid preamble key "+key+" specified" )

        self.__prm_data[ key ] = val

    def get( self, key = None ):
        if key and key not in PREAMBLE:
            raise AttributeError( "Invalid preamble key "+key+" specified" )

        if key:
            return self.__prm_data[ key ]

        return self.__prm_data

    def validate( self ):
        for p in PREAMBLE:
            if "mandatory" in PREAMBLE[p]:
                if PREAMBLE[p]['mandatory'] and p not in self.__prm_data:
                    raise LookupError( "ERROR: Missing mandatory key '" + p + "'" )
        return True

    def compile( self ):
        retlist = [""]
        for p in self.__prm_data:
            key = PREAMBLE[ p ][ 'title' ]
            if type( self.__prm_data[ p ] ).__name__ == "str":
                retlist.append( key + ": " + self.__prm_data[ p ] )
            elif type( self.__prm_data[ p ] ).__name__ == "list":
                for a,b in enumerate( self.__prm_data[ p ] ):
                    retlist.append( key + str(a) + ": " + b )

        retlist.append( "" )
        return "\n".join( retlist )


    def append_source( self, val ):
        max_val = PREAMBLE["source"]['high']
        self.__prm_data[ 'source' ].append( val )

    def append_patch( self, val ):
        max_val = PREAMBLE["patch"]['high']
        self.__prm_data[ 'patch' ].append( val )


##==============================================================================
##
##
##
##==============================================================================
class RpmSpecAbstractDirecive( ):
    def __init__( self, project_path ):
        pass

class RpmSpecPrepDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecPrepDirecive, self ).__init__( project_path )

class RpmSpecDescriptionDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecDescriptionDirecive, self ).__init__( project_path )

class RpmSpecBuildDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecBuildDirecive, self ).__init__( project_path )

class RpmSpecInstallDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecInstallDirecive, self ).__init__( project_path )

class RpmSpecCheckDirecive( RpmSpecAbstractDirecive):
    def __init__( self, project_path ):
        super(RpmSpecCheckDirecive, self ).__init__( project_path )

class RpmSpecChangelogDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecChangelogDirecive, self ).__init__( project_path )

class RpmSpecFileDirecive( RpmSpecAbstractDirecive ):
    def __init__( self, project_path ):
        super(RpmSpecFileDirecive, self ).__init__( project_path )







##==============================================================================
##
##
##
##==============================================================================
class RpmSpec():

    def __init__( self, config={} ):
        pprint( config )

        pass




##==============================================================================
##
##
##
##==============================================================================
if __name__ == "__main__":
    pprint( PREAMBLE )
    pprint( DIRECTIVES )
    pprint( SEL_MACROS )
    pprint( CONSTANTS )
    print( "----------------------" )
    spec = RpmSpecPreamble()

    spec.set( "name", "testing")
    spec.set( "version", "1.0.1")
    spec.set( "summary", "testnig")
    spec.append_source( "teste1")
    spec.append_source( "teste2")
    spec.append_source( "teste3")
    print( "----------------------" )
    pprint( spec.__dict__ )
    pprint( spec.validate() )
    print( "----------------------" )
    print( spec.compile() )
    print( "----------------------" )
