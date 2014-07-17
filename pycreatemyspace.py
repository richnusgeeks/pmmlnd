#! /usr/bin/env python
############################################################################
# File name : pycreatemyspace.py                                           #
# Purpose   : Generation of a good directories hierarchy as per user.      #
# Usages    : python pycreatemyspace.py [options] dir1 dir2 dir3 ...       #
# Start date : 14/11/2010                                                  #
# End date   : 16/11/2010                                                  #
# Author     : Ankur Kumar Sharma <richnusgeeks@gmail.com>                 #
# Download link : http://www.richnusgeeks.com                              #
# License       : GNU GPL v3 http://www.gnu.org/licenses/gpl.html          #
# Version       : 0.0.2                                                    #
# Modification history : 1. refactorization of old code with               #
#                           pygenericrouties.py by Ankur                   #
#                        2. fixed a bug regarding deriving config file     #
#                           section name when the app is invoked from other#
#                           locations by Ankur                             #
############################################################################


try:
    from pygenericroutines import PyGenericRoutines, prntErrWarnInfo
except Exception, e:
    serr = ('%s, %s' %('from pygenericroutines import PyGenericRoutines',
                         str(e)))
    prntErrWarnInfo(serr)

try:
    import os.path
except Exception, e:
    serr = '%s, %s' %('import os.path', str(e))
    prntErrWarnInfo(serr)

try:
    import sys
except Exception, e:
    serr = '%s, %s' %('import sys', str(e))
    prntErrWarnInfo(serr)


class PyCreateMySpace:
    '''
        This python module provides functionality to create directories
        hierarchy to efficiently maintain one's data/work.
    '''
    
    def __init__(self):
        '''
            Class constructor to utilize required data structurs.
        '''

        self.opygenericroutines = PyGenericRoutines(self.__class__.__name__)
        self.opygenericroutines.setupLogging()
        self.bcnfgfloprtn = self.opygenericroutines.setupConfigFlOprtn()
        self.tposargs = ('dirname',)
        self.swrkgdir    = '.'
        self.bcnfgfl     = False
        self.sclsnme     = self.__class__.__name__
        self.susage      = 'usage: %prog [options] dir1 dir2 dir3 ...'
        self.tdirs       = ()
        self.tsubdirs    = ()
        
        self.doptsargs = {
                          'dir' : {
                                   'shortopt' : '-d',
                                   'longopt'  : '--dir',
                                   'type'     : 'string',
                                   'dest'     : 'directory',
                                   'default'  : '.',
                                   'action'   : 'store',
                                   'help'     : 'set working directory',
                                  },

                          'dirs': {
                                   'shortopt' : '-p',
                                   'longopt'  : '--parents',
                                   'type'     : 'string',
                                   'dest'     : 'directories',
                                   'default'  : '',
                                   'action'   : 'store',
                                   'help'     : ('set list of directories'
                                                  + ' to be created'),
                                  },

                          'sub' : {
                                   'shortopt' : '-s',
                                   'longopt'  : '--subdirs',
                                   'type'     : 'string',
                                   'dest'     : 'subdirectories',
                                   'default'  : '',
                                   'action'   : 'store',
                                   'help'     : ('set list of'
                                                  + ' subdirectories to be'
                                                  + ' created in parents'),
                                  },

                          'configfile' : {
                                          'shortopt' : '-c',
                                          'longopt'  : '--config',
                                          'dest'     : 'configfile',
                                          'action'   : 'store_true',
                                          'help'     : ('read from config'
                                                         + ' file'),
                                         }

                         }


    def parseOptsArgs(self):
        '''
            Method to parse command line options and arguments.
        '''

        options = None
        args    = None    
        try:
            (options, args) = self.opygenericroutines.parseCmdLine(\
                                  self.doptsargs, tposargs = self.tposargs,\
                                  susage = self.susage, bminposargs = False,\
                                  bexactposargs = False)
        except Exception, e:
            serr = ('%s::parseOptsArgs(...):parseCmdLine(...), %s'
                     %(self.sclsnme, str(e)))
            self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                       smsgtype = 'err',\
                                                       bresume = True)
            return False
                                 
        if options.directory:
            self.swrkgdir = options.directory

        if options.directories:
            self.tdirs = tuple(options.directories.split())

        if options.subdirectories:
            self.tsubdirs = tuple(options.subdirectories.split())

        if options.configfile:
            self.bcnfgfl = options.configfile

        return True


    def cacheValsFromCnfgFl(self):
        '''
            method to cache various sections values from config file
            once.
        '''
        ssection = os.path.basename(sys.argv[0]).split('.')[0]
        sreturn = '' 

        if self.bcnfgfl:

            try:
                sreturn = self.opygenericroutines.getValFromConfigFl(\
                          ssection, 'Directories')
                if sreturn:
                    self.tdirs = tuple(sreturn.split())
            except Exception, e:
                serr = ('%s::cacheValsFromCnfgFl(...):\
                         getValFromConfigFl(\'Directories\'), %s'
                         %(self.sclsnme, str(e)))
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                return False

            try:
                sreturn = self.opygenericroutines.getValFromConfigFl(\
                          ssection, 'Subdirectories')
                if sreturn:
                    self.tsubdirs = tuple(sreturn.split())
            except Exception, e:
                serr = ('%s::cacheValsFromCnfgFl(...):\
                         getValFromConfigFl(\'Subdirectories\'), %s'
                         %(self.sclsnme, str(e)))
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                return False

        return True


    def createDirsHierarchy(self):
        '''
            method to create directories hierarchy as per user.
        '''

        sdirfullpth = ''
        ssubdirfullpth = ''

        for i in self.tdirs:

            sdirfullpth = os.path.join(self.swrkgdir, i)
            if self.opygenericroutines.createDirIfNotThere(i, self.swrkgdir):
                sinfo = '%s created.' %(sdirfullpth)
                prntErrWarnInfo(sinfo, smsgtype = 'info', bresume = True)
            else:
                serr = '%s not created.' %(sdirfullpth)
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                continue
                
            for j in self.tsubdirs:
                
                ssubdirfullpth = os.path.join(sdirfullpth, j)
                if self.opygenericroutines.createDirIfNotThere(j,\
                                                               sdirfullpth):
                    sinfo = '%s created.' %(ssubdirfullpth)
                    prntErrWarnInfo(sinfo, smsgtype = 'info', bresume = True)
                else:
                    serr = '%s not created.' %(ssubdirfullpth)
                    self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True) 

        return True      


def main(opycreatemyspace):
    '''
        main application driver routine.
    '''

    if opycreatemyspace.parseOptsArgs():

        opycreatemyspace.cacheValsFromCnfgFl()
        opycreatemyspace.createDirsHierarchy()


if '__main__' == __name__:
    '''
        main routine to run in case file is not imported as a module.
    '''

    opycreatemyspace = PyCreateMySpace()
    main(opycreatemyspace)  
