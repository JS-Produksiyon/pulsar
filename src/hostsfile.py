#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: hostsfile.py
    Date Created: 2024-05-07
    Date Modified: 2024-05-08
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Production"
__languages__ = ['en','de','tr']  # languages the interface has been translated into.
__nebula__ = '1.8.2'
# ================================================================================
# Check for python version
import sys, os, re, shutil

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

from elevate import elevate
from datetime import datetime

class HostsFile():
    """
    Tools to modify the host file

    :param backup: whether or not to back up the hosts file before modification
                   WARNING! This should usually be set to True, as messing with
                            a hosts file can do serious damage to your system!
    :param type  : boolean
    """
    def __init__(self, backup=True, targetFile='') -> None:
        # we have to define the path to the default hosts file first
        if sys.platform == 'win32':
            self.path = os.environ['DriverData'][:os.environ['DriverData'].rfind('\\')] + os.sep + 'etc'
        elif sys.platform == 'darwin':
            self.path = '/private/etc'
        else:
            self.path = '/etc'

        self.backup = backup
        self.backupFile = self.path + os.sep + 'hosts.pbak'
        self.comment = ''
        self.eol = '\n'
        self.file = self.path + os.sep + 'hosts'

        if not os.path.exists(self.file):
            print(f'Hosts file could not be found at {self.file}')


    def backupHostsFile(self) -> bool:
        """
        back up the hosts file
        
        :returns: boolean denoting success
        """
        try:
            shutil.copy(self.file, self.backupFile)
            return True
        except Exception as e:
            print(f'Unable to back up hosts file: {e}')
            return False


    def loadFromFile(self, fileName, targetFile = '') -> bool:
        """
        Load new IP Address / hostnames from file

        :param fileName  : filename containing pairs
        :type  fileName  : string
        :param targetFile: filename of alternative target file to add hosts to
        :type  targetFile: string
        :returns       : boolean denoting success
        """
        if not os.path.exists(fileName):
            print(f"Hosts file {fileName} not found")
            return False

        print(f"Loading hosts from file: {fileName}")

        if self.backup:
            self.backupHostsFile()

        d = datetime.now()
        dString = d.strftime('%Y-%m-%d %H:%M:%S %z')
        go = False
        out = f"{self.eol}"
        out = f'{out}{self.comment}{self.eol}' if self.comment != '' else out
        out = f'{out}# Hosts file updated programmatically on {dString}{self.eol}'

        with open(fileName, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                if self.validateHostsLine(line):
                    out = out + line.rstrip('\n').rstrip('\r') + self.eol
                    go = True
                line = f.readline()

        out = f'{out}# End of section{self.eol}'

        if go:
            return self.writeHostsFile(out, targetFile)

        return go


    def restoreHostsFile(self) -> bool:
        """
        Restores backed up hosts file to original location

        :returns: boolean denoting success
        """
        if os.path.exists(self.backupFile):
            print("Restoring hosts file to original state")
            try: 
                shutil.copy(self.backupFile, self.file)
                os.unlink(self.backupFile)
            except Exception as e:
                print(f'Unable to restore hosts file: {e}')
                return False

        return True


    def setComment(self, txt) -> None:
        """
        Sets a comment line to passed text

        :param txt: text to add
        :type  txt: str
        """
        reValidText = '^([#\w\s\,\.\$\@/\-()\*\!\&]+)$'

        if re.match(reValidText, txt):
            self.comment = txt if txt[0:1] == "#" else "# " + txt


    def validateHostsFile(self, fileName) -> bool:
        """
        validates a given hosts file

        :param fileName: full path of file to validate
        :type  fileName: string
        :returns       : boolean denoting file validity
        """
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    if not self.validateHostsLine(line):
                        return False
                    
                    line = file.readline()

            return True

        except Exception as e:
            print(f"Error opening file: {e}")
            return False


    def validateHostsLine(self, line) -> bool:
        """
        Validates a line as containing a valid
        """
        # regular expressions to check for proper hosts file lines
        reIpFour = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([\s]+)([a-zA-Z0-9]+\.?)[a-zA-Z]{2,6}([\s\t]+)?([#\w\s\,\.\$\@/\-()\*\!\&]+)?$'
        reIpSix  = '^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))([\s]+)([a-zA-Z0-9]+\.?)[a-zA-Z]{2,6}([\s\t]+)?([#\w\s\,\.\$\@/\-()\*\!\&]+)?$'
        reComment = '^#[\w\s\,\.\$\@/\-()\*\!\&]+$'

        if re.match(reIpFour, line) or re.match(reIpSix, line) or re.match(reComment, line) or line == '\n' or line == '\r\n':
            return True
        else:
            return False


    def writeHostsFile(self, data, targetFile='') -> bool:
        """
        Write data to hosts file
        
        :param data: lines to write to hosts file
        :type  data: string
        """
        if targetFile == '':
            targetFile = self.file

        try:
            with open(targetFile, 'a', encoding='utf-8') as f:
                f.write(data)

        except Exception as e:
            print(f'Unable to write hosts file: {e}')
            return False
        
        return True


if __name__ == "__main__":
    print('This module is not meant to be run on its own. Please call it using from hostsfile import HostsFile.')
    # elevate()
    h = HostsFile()
    srcFile = os.path.dirname(__file__) + '\\..\\creds\\hosts'
    print(h.validateHostsFile(srcFile))
    # tgtFile = os.path.dirname(__file__) + '\\..\\hosts'
    # h.setComment('Hosts entries added by Pulsar')

    # #print("Loaded hosts file: " + h.loadFromFile(srcFile))
    # print("Restored hosts file: " + h.restoreHostsFile())
    # input('Press Enter to continue')