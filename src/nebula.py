# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: nebula.py
    Date Created: 2024-05-03
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
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

import os, subprocess, yaml, signal, re
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

    def __init__(self, config='', test=False) -> None:
        """ Class initialization """
        # status variables
        self.validConfig = False
        self.connected = False
        self.nProcess = False
        self.configPath = ''
        self.configFile = ''
        self.testMode = test
        self.setConfig(config)
        self.validConfig = self.validateConfig()

    
    def connect(self) -> None:
        """
        runs the nebula binary

        :param configFile: full path to the config file
        :type  configFile: string
        """
        nPathBase = os.path.dirname(__file__) + os.sep + 'bin' + os.sep + '{os}' + os.sep + '{binary}'
        showShell = True

        # load proper binary
        if sys.platform == 'darwin':
            nPath = nPathBase.format(os='macos', binary='nebula')
        elif sys.platform == 'win32':
            nPath = nPathBase.format(os='windows', binary='nebula.exe')
        else:
            return False 
            # because this application does not work with Linux!

        if self.validConfig:
            if self.testMode:
                elevate()
                showShell = False

            if self.configPath != '':
                os.chdir(self.configPath)

            print(f'Starting Nebula client at {nPath}')
            self.nProcess = subprocess.Popen([nPath, '-config' ,self.configFile])


    def disconnect(self) -> None:
        """
        stops the nebula binary
        """
        if self.nProcess:
            print('Stopping Nebula client...')
            os.kill(self.nProcess.pid, signal.SIGINT)
            self.nProcess = False
            print('Nebula client is no longer running.')


    def setConfig(self, config) -> None:
        """
        sets a new configuration file

        :param config: path to config file
        :type  config: str
        """
        if os.path.exists(config):
            self.configFile = config
            self.configPath = self.configFile[:self.configFile.rfind(os.sep)] if os.sep in self.configFile else ''

        self.validConfig = self.validateConfig()

        if not self.validConfig:
            self.configFile = ''            
            self.configPath = ''


    def validateConfig(self) -> bool:
        """
        validates the object config file
        
        :returns: boolean denoting validity
        """
        if os.path.exists(self.configFile):
            try:
                with open(self.configFile, 'r', encoding='utf-8') as cf:
                    config = yaml.safe_load(cf)
                
                if self.configPath != '':
                    os.chdir(self.configPath)
                    
                if os.path.exists(config['pki']['ca']) and os.path.exists(config['pki']['cert']) and os.path.exists(config['pki']['key']):
                    return True
            except:
                return False

        return False


    def version(self) -> str:
        """
        Returns the version of tue current Nebula binary
        """
        # load proper binary
        nPathBase = os.path.dirname(__file__) + os.sep + 'bin' + os.sep + '{os}' + os.sep + '{binary}'

        if sys.platform == 'darwin':
            nPath = nPathBase.format(os='macos', binary='nebula')
        elif sys.platform == 'win32':
            nPath = nPathBase.format(os='windows', binary='nebula.exe')
        else:
            return False 
            # because this application does not work with Linux!

        out = []
        with subprocess.Popen([nPath, '-version'], stdout=subprocess.PIPE) as p:
            while p.poll() is None:
                out.append(p.stdout.read())
            return out[0].decode('utf-8')[9:-1]



class StayConnected():
    """
    Keeps the connection to the nebula network alive

    :param ips     : IP v4 or v6 addresses to ping to check for live connection
    :type  ips     : list
    :param task    : function to trigger when disconnection is detected
    :type  task    : reference to function
    :param interval: how often to ping in seconds (default: 300s = 5 min)
    :type  interval: integer
    """

    def __init__(self, ips, task, interval=300) -> None:
        self.active = False
        self.ipList = []
        self.pingInterval = interval if type(interval) == int else 300
        self.reconnectFunction = task

        # load and validate IPs
        if type(ips) == str:
            if self.__validateIp(ips): 
                self.ipList.append(ips)
        elif type(ips) == list:
            for ip in ips:
                if self.__validateIp(ip):
                    self.ipList.append(ip)


    def __validateIp(self, ip) -> bool:
        """
        private function to validate an IP address.

        :param ip: IP address to validate
        :type  ip: string
        :returns : boolean denoting validity
        """
        reIpFour = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        reIpSix  = '^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$'

        if type(ip) == str:
            if re.match(reIpFour, ip) or re.match(reIpSix, ip):
                return True
            else:
                return False

        return False
        

    def disable(self) -> None:
        """
        Disables keeping the connection up on disconnect
        """
        self.active = False


    def enable(self) -> bool:
        """
        Enables keeping the connection up on disconnect

        :returns : boolean to denote whether activated or not
        """
        # make sure we have valid ip addresses to process
        if len(self.ipList) < 1:
            self.active = False
            return False


    def ping(self, ip, count=3, verbose=False) -> dict:
        """
        Executes the actual ping function

        :param ip     : IP address to ping
        :type  ip     : string
        :param count  : how many pings to send (default is 3)
        :type  count  : integer
        :param verbose: whether or not to return all replies
        :type  verbose: boolean
        :returns      : dictionary as follows {result: bool, output: [list]}
        """
        data = []
        result = False
        p = subprocess.Popen(f"ping {ip} -n {count}", stdout=subprocess.PIPE, encoding='utf-8')

        for line in p.stdout:
            if 'TTL' in line:
                result = True
                data.append(line)

        return { 'result': result, 'output': data } if verbose else { 'result': result }



if __name__ == '__main__':
    print("This module is not meant to be called by itself unless testing. Please import using from nebula import Nebula.")

    try:
        if sys.platform == 'darwin':
            cf = '/Users/wolfhawke/Repositories/pulsar/creds/joshw-config.yaml'
        elif sys.platform == 'win32':
            cf = 'C:\\Users\\wolfh\\Repositories\\pulsar\\creds\\joshw-config.yaml'

        n = Nebula(cf, test=True)
        # n.connect()
        # sleep(10)
        # n.disconnect()

        ips = ['192.168.3.1']

        p = StayConnected(ips=ips, task=n.connect)
        print(p.ping(ips[0], verbose=True))

    except SystemExit:
        pass


