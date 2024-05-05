#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: nebula.py
    Date Created: 2024-05-03
    Date Modified: 2024-05-05
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en','de','tr']  # languages the interface has been translated into.
__build__ = ''
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

import os, subprocess, yaml, signal
from elevate import elevate
from time import sleep

class Nebula():
    """
    Class to control the Nebula client
    
    :param config: Path to Nebula config.yaml file
    :type  config: string
    :param test  : Whether or not we're testing this module; executes elevate in Nebula.connect
    :type  test  : boolean
    """

    def __init__(self, config, test=False) -> None:
        """ Class initialization """
        # status variables
        self.validConfig = False
        self.connected = False
        self.nProcess = False
        self.configPath = ''
        self.configFile = ''
        self.testMode = test

        if os.path.exists(config):
            self.configFile = config
            self.configPath = self.configFile[:self.configFile.rfind(os.sep)] if os.sep in self.configFile else ''
            
        self.validConfig = self.validateConfig()

    
    def connect(self) -> None:
        """
        runs the nebula binary

        :param configFile: full path to the config file
        :type  configFile: string
        """
        nPathBase = os.path.dirname(__file__) + os.sep + 'bin' + os.sep + '{os}' + os.sep + '{binary}'

        # load proper binary
        if sys.platform == 'darwin':
            nPath = nPathBase.format(os='macos', binary='nebula')
        elif sys.platform == 'win32':
            nPath = nPathBase.format(os='windows', binary='nebula.exe')
        else:
            return False 
            # because this application does not work with Linux!

        if self.validConfig:
            if self.configPath != '':
                os.chdir(self.configPath)

            if self.testMode:
                elevate()
            self.nProcess = subprocess.Popen(f'{nPath} -config {self.configFile}', shell=True)


    def disconnect(self) -> None:
        """
        stops the nebula binary
        """
        if self.nProcess:
            self.nProcess.send_signal(signal.CTRL_C_EVENT)
            self.nProcess = False


    def validateConfig(self) -> bool:
        """
        validates the object config file
        
        :returns: boolean denoting validity
        """
        if os.path.exists(self.configFile):
            with open(self.configFile, 'r', encoding='utf-8') as cf:
                config = yaml.safe_load(cf)
            
            if self.configPath != '':
                os.chdir(self.configPath)
                
            if os.path.exists(config['pki']['ca']) and os.path.exists(config['pki']['cert']) and os.path.exists(config['pki']['key']):
                return True

        return False


if __name__ == '__main__':
    print("This module is not meant to be called by itself unless testing. Please import using from nebula import Nebula.")

    try:
        n = Nebula('C:\\Users\\wolfh\\Repositories\\pulsar\\creds\\joshw-config.yaml', test=True)
        n.connect()
        sleep(10)
        n.disconnect()
    except SystemExit:
        pass