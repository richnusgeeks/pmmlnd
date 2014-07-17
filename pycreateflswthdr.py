#! /usr/bin/env python
############################################################################
# File name : pycreateflswthdr.py                                          #
# Purpose   : Generation of various source/header files with info header.  #
# Usages    : python pycreateflswthdr.py [options] filename1.ext1 ...      #
# Start date : 12/11/2010                                                  #
# End date   : 14/11/2010                                                  #
# Author     : Ankur Kumar Sharma <richnusgeeks@gmail.com>                 #
# Download link : http://www.richnusgeeks.com                              #
# License       : GNU GPL v3 http://www.gnu.org/licenses/gpl.html          #
# Version       : 0.0.6                                                    #
# Modification history : 1. addition of cacheValsFromCnfgFls(...) in 0.0.3 #
#                           by Ankur                                       #
#                        2. fixed a bug regarding deriving config file     #
#                           section name when the app is invoked from other#
#                           locations by Ankur                             #
#                        3. a change to get login name on both Linux & Win #
#                           by Ankur.                                      #
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


class PyCreateFlsWthdr():

    '''
        This class provides the functionalities to create/append the
        info headers and then generate various kinds of source/header files.
    '''

    def __init__(self):
        '''
            Class constructor to initialize required data structures.
        '''
        
        self.opygenericroutines = PyGenericRoutines(self.__class__.__name__)
        self.opygenericroutines.setupLogging()
        self.bcnfgfloprtn = self.opygenericroutines.setupConfigFlOprtn()
        self.tposargs    = ('filename.ext',)
        self.tvldfls     = ()
        self.sflextn     = ''
        self.swrkgdir    = '.'
        self.bapnd       = False
        self.bcnfgfl     = False
        self.sflnme      = ''
        self.sclsnme     = self.__class__.__name__
        self.sathrnme    = os.getenv('USERNAME')
        self.sdwnldlnk   = 'http://www.%s.com' %(socket.gethostname())
        self.slcnsnme    = 'GNU GPL v3 http://www.gnu.org/licenses/gpl.html'
        self.sversion    = 'major.minor.release'
        self.dcmntsymnum = {
                            ('c', 'h', 'cpp', 'hpp', 'java',) : {
                                                                 'symbol' : '//',
                                                                 'count'  : 38,
                                                                },
                            ('py', 'pl', 'rb', 'sh', 'php', 'mak',) : {
                                                                       'symbol' : '#',
                                                                       'count'  : 76,
                                                                      },
                            ('lua', 'sql',) : {
                                               'symbol' : '--',
                                               'count'  : 38,
                                              }
                           }
        self.doptsargs = {
                           'dir' : {
                                    'shortopt' : '-d',
                                    'longopt'  : '--dir',
                                    'type'     : 'string',
                                    'dest'     : 'directory',
                                    'default'  : '.',
                                    'action'   : 'store',
                                    'help'     : 'sets working directory',
                                   },
                            
                           'append' : {
                                       'shortopt' : '-a',
                                       'longopt'  : '--append',
                                       'dest'     : 'appendflag',
                                       'action'   : 'store_true',
                                       'help'     : 'append info header',
                                      },

                           'configfile' : {
                                           'shortopt' : '-c',
                                           'longopt'  : '--config',
                                           'dest'     : 'configfile',
                                           'action'   : 'store_true',
                                           'help'     : 'read from config file'
                                          }
                            
                         }

        self.susage = 'usage: %prog [options] filename1.ext1 filename2.ext2 ...'
        self.thdrttls = (
                         'File name',
                         'Purpose',
                         'Usages',
                         'Start date',
                         'End date',
                         'Author',
                         'Download link',
                         'License',
                         'Version',
                         'Modification history',
                        )
        self.dintrprtrs = {
                           'py' : 'python',
                           'pl' : 'perl',
                           'sh' : 'bash',
                           'rb' : 'ruby',
                           'lua': 'lua',
                          }
        self.senvpath   = '#! /usr/bin/env' 
 

    def parseOptsArgs(self):
        '''
            Method to parse command line options and arguments.
        '''

        options = None
        args    = None
        try:
            (options, args) = self.opygenericroutines.parseCmdLine(         \
                                  self.doptsargs, tposargs = self.tposargs ,\
                                  susage = self.susage, bminposargs = True, \
                                  bexactposargs = False)
        except Exception, e:
            serr = (self.sclsnme + '::' + 'parseOptsArgs(...)' + ':'
                    + 'parseCmdLine(...)' + ', ' + str(e))
            self.opygenericroutines.prntLogErrWarnInfo(serr, smsgtype = 'err', bresume = True)
            return False

        if options.directory:
            self.swrkgdir = options.directory

        if options.appendflag:
            self.bapnd = options.appendflag

        if options.configfile:
            self.bcnfgfl = options.configfile

        self.tposargs = tuple(args)
        
        return True


    def isFlwtValidExtn(self, sflnme):
        '''
            Method to test the validity of a file extension.
        '''
        
        lflnm = sflnme.split('.')
        sextn = lflnm[-1].lower()
    
        for i in self.dcmntsymnum:
            if len(lflnm) > 1 and sextn in i:
                return True

        return False     


    def verifyAndBackup(self):
        '''
            Method to verify the validity of options and arguments and backup existing files.
        '''

        lvldfls = []
        for i in self.tposargs:
            if self.isFlwtValidExtn(i):
                lvldfls.append(i)
                try:
                    if self.opygenericroutines.doesFileExist(i, self.swrkgdir): 
                        try:
                            if not self.opygenericroutines.backupFile(i, self.swrkgdir):
                                return False
                        except Exception, e:
                            serr = (self.sclsnme + '::' + 'verifyAndBackup(...)' + ':'
                                    + 'backupFile(...)' + ', ' + str(e))           
                            self.opygenericroutines.prntLogErrWarnInfo(serr, smsgtype = 'err', bresume = True)
                            return False
                except Exception, e:
                    serr = (self.sclsnme + '::' + 'verifyAndBackup(...)' + ':'
                            + 'doesFileExist(...)' + ', ' + str(e))
                    self.opygenericroutines.prntLogErrWarnInfo(serr, smsgtype = 'err', bresume = True)
                    return False
            else:
                swarn = (self.sclsnme + '::' + 'verifyAndBackup(...)' + ':'
                         + 'file ' + str(i) + ' is not having a valid extension, so skipping.')
                self.opygenericroutines.prntLogErrWarnInfo(swarn, smsgtype = 'warn', bresume = True)

        self.tvldfls = tuple(lvldfls)
        return True    


    def createFlwtInfoHdr(self, sflnme):
        '''
            method to prepare and write/append info header string according
            to the file type.
        '''

        sflcntnt = ''
        sinfohdr = ''
        scmntsym = ''
        uicount   = 0
        sflextn = sflnme.split('.')[-1].lower()
       
        for i in self.dcmntsymnum:
            if sflextn in i:
                scmntsym = self.dcmntsymnum[i]['symbol']
                uicount  = self.dcmntsymnum[i]['count']

        if sflextn in self.dintrprtrs:
            sinfohdr = self.senvpath + ' ' + self.dintrprtrs[sflextn] + '\n' 
                
        sstrtdte = ''
        senddte  = ''
        try:
            sstrtdte = time.strftime("%d/%m/%Y", time.gmtime())
            senddte  = time.strftime("dd/mm/%Y", time.gmtime())
        except Exception, e:
            serr = (self.sclsnme + '::' + 'createFlwtInfoHdr(...)' + ':'
                    + 'strftime(...)' + ', ' + str(e))
            self.opygenericroutines.prntLogErrWarnInfo(serr, \
                                                       smsgtype = 'err', \
                                                       bresume = True)
            return False

        try:
            sflfullpth = os.path.join(self.swrkgdir, sflnme)
        except Exception, e:
            serr = (self.sclsnme + '::' + 'createFlwtInfoHdr(...)' + ':'
                    + 'join(...)' + ', ' + str(e))
            self.opygenericroutines.prntLogErrWarnInfo(serr, \
                                                       smsgtype = 'err', \
                                                       bresume = True)
            return False
        
        ofl = None
        if self.bapnd:
            try:
                ofl = open(sflfullpth, 'rb')
                if ofl:
                    sflcntnt = ofl.read()
                    ofl.close()
            except Exception, e:
                serr = (self.sclsnme + '::' + 'createFlwtInfoHdr(...)' + ':'
                        + 'open, read, close(...)' + ', ' + str(e))
                self.opygenericroutines.prntLogErrWarnInfo(serr, \
                                                          smsgtype = 'err', \
                                                          bresume = True)
                return False

        sinfohdr += scmntsym * uicount + '\n'
        for i in self.thdrttls:
            if 'File name' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, sflnme)
            elif 'Start date' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, sstrtdte)
            elif 'End date' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, senddte)
            elif 'Author' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, self.sathrnme)
            elif 'Download link' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, self.sdwnldlnk)
            elif 'License' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, self.slcnsnme)
            elif 'Version' == i:
                sinfohdr += '%s %s : %s\n' %(scmntsym, i, self.sversion)            
            else:    
                sinfohdr += '%s %s : \n' %(scmntsym, i)
        
        if self.bapnd:
            sinfohdr += '%s\n\n%s\n' %(scmntsym * uicount, sflcntnt)
        else:
            sinfohdr += '%s\n' %(scmntsym * uicount)

        ofl = None
        try:
            ofl = open(sflfullpth, 'wb')
            ofl.write(sinfohdr)
            ofl.close()
        except Exception, e:
            serr = (self.sclsnme + '::' + 'createFlwtInfoHdr(...)' + ':'
                    + 'open, write, close(...)' + ', ' + str(e))
            self.opygenericroutines.prntLogErrWarnInfo(serr, \
                                                       smsgtype = 'err', \
                                                       bresume = True)
            return False

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
                          ssection, 'Author')
                if sreturn:
                    self.sathrnme = sreturn.strip()
            except Exception, e:
                serr = ('%s::cacheValsFromCnfgFl(...):\
                         getValFromConfigFile(\'Author\'), %s'
                         %(self.sclsnme, str(e)))
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                return False
                
            try:
                sreturn = self.opygenericroutines.getValFromConfigFl(\
                          ssection, 'Download link')
                if sreturn:
                    self.sdwnldlnk = sreturn.strip()
            except Exception, e:
                serr = ('%s::cacheValsFromCnfgFl(...):\
                         getValFromConfigFile(\'Download link\'), %s'
                          %(self.sclsnme, str(e)))
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                return False
            
            try:
                sreturn = self.opygenericroutines.getValFromConfigFl(\
                          ssection, 'License')
                if sreturn:
                    self.slcnsnme = sreturn.strip()
            except Exception, e:
                serr = ('%s::cacheValsFromCnfgFl(...):\
                         getValFromConfigFile(\'License\'), %s'
                         %(self.sclsnme, str(e)))
                self.opygenericroutines.prntLogErrWarnInfo(serr,\
                                                           smsgtype = 'err',\
                                                           bresume = True)
                return False

        return True


def mainconsole(opycreateflswthdr):
    '''
        main application driver routine for console mode.
    '''

    if opycreateflswthdr.parseOptsArgs():
        
        if opycreateflswthdr.verifyAndBackup():

            opycreateflswthdr.cacheValsFromCnfgFl()
        
            for i in opycreateflswthdr.tvldfls:
                
                if opycreateflswthdr.createFlwtInfoHdr(i):

                    sflfullpth = os.path.join(opycreateflswthdr.swrkgdir, i)
                    
                    if opycreateflswthdr.bapnd:
                        sinfo = '%s %s'%(sflfullpth, 'appended succesfully.')
                    else:
                        sinfo = '%s %s'%(sflfullpth, 'created succesfully.')
                         
                    prntErrWarnInfo(sinfo, smsgtype = 'info', bresume = True) 



if '__main__' == __name__:
    '''
        routine to run in case file is not imported as a module.
    '''

    opycreateflswthdr = PyCreateFlsWthdr()
    mainconsole(opycreateflswthdr)
