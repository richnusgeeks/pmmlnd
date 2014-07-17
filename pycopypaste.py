#! /usr/bin/env python
############################################################################
# File name : pycopypaste.py                                               #
# Purpose   : Append/Insert text of one file into another.                 #
# Usages    : python pycopypaste.py [options] arguments source             #
# Start date : 01/08/2011                                                  #
# End date   : dd/08/2011                                                  #
# Author     : Ankur Kumar Sharma <richnusgeeks@gmail.com>                 #
# Download link : http://www.richnusgeeks.com                              #
# License       : GNU GPL v3 http://www.gnu.org/licenses/gpl.html          #
# Version       : 0.0.1                                                    #
# Modification history :                                                   #
############################################################################


def _prntErrWarnInfo(smsg, smsgtype = 'err', bresume = False):
    '''
        Global routine to print error/warning/info strings and resume/exit.
    '''

    derrwarninfo = {
                    'err'  : ' ERROR',
                    'warn' : ' WARNING',
                    'info' : ' INFO',
                   }  

    if not isinstance(smsg, str):

        print
        print (' Error : Invalid message type, '
               + 'please enter string.')
        print
        return False

    if smsgtype not in derrwarninfo.keys():
        
        print
        print (' Error : Invalid message type, '
               + 'please choose from \'err\', \'warn\', \'info\'.')
        print
        return False

    print
    print derrwarninfo[smsgtype] + ' : ' + smsg
    print

    if not bresume:
        print ' exiting ...'
        exit(-1)
    else:
        return True


try:
    from pygenericroutines import PyGenericRoutines, prntErrWarnInfo
except Exception, e:
    serr = ('%s, %s'
            %('from pygenericroutines import PyGenericRoutines', str(e)))
    _prntErrWarnInfo(serr)

try:
    import os
except Exception, e:
    serr = '%s, %s' %('import os', str(e))
    prntErrWarnInfo(serr)

try:
    import os.path
except Exception, e:
    serr = '%s, %s' %('import os.path', str(e))
    prntErrWarnInfo(serr)

try:
    import socket
except Exception, e:
    serr = '%s, %s' %('import socket', str(e))

try:
    import time
except Exception, e:
    serr = '%s, %s' %('import time', str(e))
    prntErrWarnInfo(serr)

try:
    import sys
except Exception, e:
    serr = '%s, %s' %('import sys', str(e))
    prntErrWarnInfo(serr)


class PyCopyPaste:
    '''
        This class provides some of the functionality similar to sed and
        awk in Pythonic and Portable way.
    '''
    
    def __init__(self):
        '''
            Class constructor to initialize required data structures.
        '''

        self.__sclsnme = self.__class__.__name__
        self.__opygenericroutines = PyGenericRoutines(self.__sclsnme)
        self.__opygenericroutines.setupLogging()
        self.__bcnfgfloprtn = self.__opygenericroutines.setupConfigFlOprtn()
        self.__doptsargs = {
                            'srcdir' : {
                                         'shortopt' : '-s',
                                         'longopt'  : '--srcdir',
                                         'type'     : 'string',
                                         'dest'     : 'srcdir',
                                         'default'  : '.',
                                         'action'   : 'store',
                                         'help'     : 'sets source directory',
                                        },
                            'trgtdir' : {
                                         'shortopt' : '-t',
                                         'longopt'  : '--trgtdir',
                                         'type'     : 'string',
                                         'dest'     : 'trgtdir',
                                         'default'  : '.',
                                         'action'   : 'store',
                                         'help'     : 'sets target directory',
                                        },
                            'append'  : {
                                         'shortopt' : '-a',
                                         'longopt'  : '--append',
                                         'dest'     : 'appendflag',
                                         'action'   : 'store_true',
                                         'help'     : 'append from source',
                                        },
                            'insert'  : {
                                         'shortopt' : '-i',
                                         'longopt'  : '--insert',
                                         'dest'     : 'insertflag',
                                         'action'   : 'store_true',
                                         'help'     : 'insert from source',
                                        },
                            'confgfle': {
                                          'shortopt': '-c',
                                          'longopt' : '--config',
                                          'dest'    : 'configfile',
                                          'action'  : 'store_true',
                                          'help'    : 'read from config file',
                                        },   
                           'strtendsrc':{
                                         'shortopt' : '-f',
                                         'longopt'  : '--strtendsrc',
                                         'type'     : 'int',
                                         'dest'     : 'strtendsrc',
                                         'nargs'    : 2,
                                         'action'   : 'store',
                                         'help'     : 'start & end lines from source',
                                        },
                          'strttrgt':{
                                         'shortopt' : '-d',
                                         'longopt'  : '--strttrgt',
                                         'type'     : 'int',
                                         'dest'     : 'strttrgt',
                                         'default'  : 1,
                                         'action'   : 'store',
                                         'help'     : 'start line for target',                                    },
                           }

  
        self.__susage = 'usage: %prog [options] sourcefile -f startlinenum endlinenum targetfile -d startlinenum -i|-a'

        self.__ssrcdir  = '.'
        self.__strgtdir = '.'
        self.__ssrcfle  = ''
        self.__strgtfle = ''
        self.__ssrcflewpth = ''
        self.__strgtflewpth = ''

        self.__dstlnnum = {
                           'source' : {
                                       'start' : 1,
                                       'end'   : 1,
                                      },
                           'target' : {
                                       'start' : 1,
                                      },
                          }
        self.__bappend = False
        self.__binsert = False
        self.__tposargs= ('sourcefile', 'trgtfile',)

        self.__osrcfile = None
        self.__lsrcfile = []
        self.__nsrclnes = 0
        self.__otrgtfile = None
        self.__ltrgtfile = []
        self.__ntrgtlnes = 0
        self.__ldsrdlnes = []              

                          
    def parseOptsArgs(self):
        '''
            Method to parse command line options and arguments.
        '''

        options = None
        args    = None
        try:
            (options, args) = self.__opygenericroutines.parseCmdLine(      \
                              self.__doptsargs, tposargs = self.__tposargs,\
                              susage = self.__susage)                                                               
        except Exception, e:
            serr = ("%s::parseOptsArgs(...):parseCmdLine(...), %s"
                     %(self.__sclsnme, str(e)))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, smsgtype = 'err', bresume = True)
            return False

        if options.srcdir:
            self.__ssrcdir = options.srcdir

        if options.trgtdir:
            self.__strgtdir = options.trgtdir

        if options.appendflag:
            self.__bappend = options.appendflag
        
        if options.insertflag:
            self.__binsert = options.insertflag

        if options.strtendsrc:
            self.__dstlnnum['source']['start'] = min(options.strtendsrc)
            self.__dstlnnum['source']['end']   = max(options.strtendsrc)

        if options.strttrgt:
            self.__dstlnnum['target']['start'] = options.strttrgt

        self.__tposargs = tuple(args)

        return True


    def verifyOptsArgs(self):
        '''
            Method to verify all the options and arguments.
        '''

        self.__ssrcflewpth = os.path.join(self.__ssrcdir,
                                          self.__tposargs[0])

        self.__strgtflewpth = os.path.join(self.__strgtdir,
                                           self.__tposargs[1])

        if not self.__opygenericroutines.doesFileExist(self.__tposargs[0],
                                                        self.__ssrcdir):
            serr = ('%s::verifyOptsArgs(...):%s does not exist'
                     %(self.__sclsnme, self.__ssrcflewpth))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        if not self.__opygenericroutines.doesFileExist(self.__tposargs[1],
                                                        self.__strgtdir):
            serr = ('%s::verifyOptsArgs(...):%s does not exist'
                     %(self.__sclsnme, self.__strgtflewpth))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        if self.__bappend is True and self.__binsert is True:
            serr = ('%s::verifyOptsArgs(...):both append as well as insert flags not applicable at same time' %(self.__sclsnme))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        if not self.__bappend and not self.__binsert:
            serr = ('%s::verifyOptsArgs(...):neither append nor insert flag was supplied' %(self.__sclsnme))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        try:
            self.__osrcfile = open(self.__ssrcflewpth, 'rb')
        except Exception, e:
            serr = ('%s::verifyOptsArgs(...):open(%s), %s'
                     %(self.__sclsnme, self.__ssrcflewpth, str(e)))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        try:
            self.__lsrcfile = self.__osrcfile.readlines()
        except Exception, e:
            serr = ('%s::verifyOptsArgs(...):readlines(%s), %s'
                     %(self.__sclsnme, self.__ssrcflewpth, str(e)))
            self.__opygenericroutines.prntErrWarnInfo(serr, 'err', bresume = True)
            return False

        if len(self.__lsrcfile) < self.__dstlnnum['source']['start'] \
           or len(self.__lsrcfile) < self.__dstlnnum['source']['end']:
            serr = ('%s::verifyOptsArgs(...):%s start or end index exceeds file size.' 
                     %(self.__sclsnme, self.__ssrcflewpth))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False
  
        self.__osrcfile.close()   
                       
        try:
            self.__otrgtfile = open(self.__strgtflewpth, 'rb')
        except Exception, e:
            serr = ('%s::verifyOptsArgs(...):open(%s), %s'
                     %(self.__sclsnme, self.__strgtflewpth, str(e)))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        try:
            self.__ltrgtfile = self.__otrgtfile.readlines()
        except Exception, e:
            serr = ('%s::verifyOptsArgs(...):readlines(%s), %s'
                     %(self.__sclsnme, self.__strgtflewpth, str(e)))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
            return False

        self.__otrgtfile.close()   

        if self.__binsert:
            if len(self.__ltrgtfile) < self.__dstlnnum['target']['start']:
                serr = ('%s::verifyOptsArgs(...):%s start index exceeds file size.' 
                         %(self.__sclsnme, self.__strgtflewpth))
                self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err', bresume = True)
                return False

        self.__ldsrdlnes = self.__lsrcfile[self.__dstlnnum['source']['start']-1 : self.__dstlnnum['source']['end']]

        return True


    def getState(self):
        '''
            Method to reflect current object state.
        '''

        print(' __ssrcdir  : %s' %(self.__ssrcdir))
        print(' __strgtdir : %s' %(self.__strgtdir))
        print(' __bappend  : %s' %(self.__bappend))
        print(' __binsert  : %s' %(self.__binsert))
        print(' __tposargs : %s' %(str(self.__tposargs)))
        print(' __dstlnnum : %s' %(str(self.__dstlnnum)))
        print(' __lsrcfile : %s' %(str(self.__lsrcfile)))
        print(' __ltrgtfile : %s' %(str(self.__ltrgtfile)))
        print(' __ldsrdlnes : %s' %(str(self.__ldsrdlnes)))


    def copyOrPaste(self):
        '''
            Method to copy or paste the desired lines
            from the source file to the target file.
        '''

        if not self.__opygenericroutines.backupFile(self.__tposargs[1],
                                                    self.__strgtdir):
            serr = ('%s::copyOrPaste(...):%s backup failed'
                     %(self.__sclsnme, self.__strgtflewpth))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err',
                                                         bresume = True)
            return False

        
        try:
            self.__otrgtfile = open(self.__strgtflewpth, 'wb')
        except Exception, e:
            serr = ('%s::copyOrPaste(...):open(%s), %s'
                     %(self.__sclsnme, self.__strgtflewpth, str(e)))
            self.__opygenericroutines.prntLogErrWarnInfo(serr, 'err',
                                                         bresume = True)
            return False

        if self.__bappend:
            self.__otrgtfile.writelines(self.__ltrgtfile + ['\n'] + \
                                        self.__ldsrdlnes + ['\n'])

        if self.__binsert:
            self.__otrgtfile.writelines(
               self.__ltrgtfile[0 : self.__dstlnnum['target']['start']-1] \
               + ['\n'] + self.__ldsrdlnes + ['\n'] + \
               self.__ltrgtfile[self.__dstlnnum['target']['start']-1 :]) 

        if not self.__otrgtfile:
            self.__otrgtfile.close()

        return True
          

def mainconsole(opycopypaste):
    '''
        Main application driver routine for console mode.
    '''

    if opycopypaste.parseOptsArgs():
        
        if opycopypaste.verifyOptsArgs():

            if not opycopypaste.copyOrPaste():

                serr = 'mainconsole(...):copyOrPaste(...) failed.'
                _prntErrWarnInfo(serr, 'err', bresume = True)

        else:
            serr = 'mainconsole(...):verifyOptsArgs(...) failed.'
            _prntErrWarnInfo(serr, 'err', bresume = True)

    else:
        serr = 'mainconsole(...):parseOptsArgs(...) failed.'
        _prntErrWarnInfo(serr, 'err', bresume = True)          
 

if '__main__' == __name__:
    '''
        Routine to run in case file is not imported as a module.
    '''

    opycopypaste = PyCopyPaste()
    mainconsole(opycopypaste)
