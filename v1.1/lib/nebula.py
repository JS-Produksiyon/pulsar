# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: nebula.py
    Date Created: 2024-05-03
    Date Modified: 2024-07-01
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.1.1"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en','de','tr']  # languages the interface has been translated into.
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

import os, subprocess, yaml, signal, re, threading, random
from elevate import elevate
from time import sleep
import logging

# use this to refer to logging levels
LOGLEVELS = {
    'debug'   : logging.DEBUG,
    'info'    : logging.INFO,
    'warning' : logging.WARNING,
    'error'   : logging.ERROR,
    'critical': logging.CRITICAL
    }

class Nebula():
    """
    Class to control the Nebula client
    
    :param config    : Path to Nebula config.yaml file
    :type  config    : string
    :param keep_alive: Whether or not to keep the nebula connection alive; defaults to True
    :type  keep_alive: boolean
    :param log_file  : path to log file; defaults to nebula.py in current directory
    :type  log_file  : string
    :param test      : Whether or not we're testing this module; executes elevate in Nebula.connect
    :type  test      : boolean
    """

    def __init__(self, config='', keep_alive=True, log_file='nebula.log', log_level='info', test=False) -> None:
        """ Class initialization """
        # status variables
        self.validConfig = False
        self.connected = False
        self.nProcess = False
        self.configPath = ''
        self.configFile = ''
        self.keepAlive = keep_alive if type(keep_alive) == bool else True
        self.logFile = log_file
        self.logLevel = log_level if log_level in ['debug', 'info', 'warning', 'error', 'critical'] else 'info'  # sets logging level
        self.usePing = True        # whether or not to use the ping method to check for updates
        self.pingInterval = 300    # ping interval to use
        self.pingTargets = []      # ip addresses to ping
        self.testMode = test
        self.threadEvent = threading.Event()
        self.setConfig(config)
        self.validConfig = self.validateConfig()
        
        # set up logging
        self.logger = logging.getLogger(__name__)
        loggerString = '{"level": "%(levelname)s", "msg": "%(message)s", "time":"%(asctime)s"}'  # JSON-based
        # loggerString = '[%(asctime)s] %(levelname)s :: %(message)s'                             # Text-based
        logging.basicConfig(filename=self.logFile, encoding='utf-8', format=loggerString, level=LOGLEVELS[self.logLevel])


    def __checkConnect(self) -> None:
        """
        private method that checks if the connection is currently alive
        """
        self.logger.debug(f'Keep Connection Alive: {self.keepAlive}')
        checkInterval = 3    # every how many seconds we check for the running process
        currentInterval = 0  # how many seconds have elapsed to pingInterval

        while self.keepAlive:
            sleep(3)
            # this needs to be first so it triggers before any checks if user shuts down the connection
            if self.threadEvent.is_set():
                self.logger.debug('Nebula connection is terminated by thread event. Ending keepAlive thread.')
                self.threadEvent.clear()
                break

            # make sure that the process is still running
            self.logger.debug(f'Expected connection status: {self.connected}; Actual process status: {self.nProcess}')
            if self.connected and not self.nProcess:
                self.logger.info('Nebula connection was interrupted. keepAlive thread is active. Restarting nebula.')
                self.restartConnection()

            # also try by accessing the pid
            try: 
                self.logger.debug(f'Nebula PID: {self.nProcess.pid}')
            except:
                self.logger.info('Nebula connection was interrupted. keepAlive thread is active. Restarting nebula.')
                self.restartConnection()

            currentInterval = currentInterval + checkInterval

            # check for connectivity using ping according to self.pingInterval
            if self.usePing and currentInterval >= self.pingInterval:
                currentInterval = 0
                ip = self.pingTargets[random.randint(0,(len(self.pingTargets)-1))]
                self.logger.debug(f'Checking connection status by pinging {ip}')
                p = self.ping(ip)
                if not p['result']:
                    self.logger.warning(f'Nebula network ping check to {ip} failed. Restarting nebula connection.')
                    self.restartConnection()
                self.logger.debug('Ping complete. Result: {}'.format('Ping received' if p['result'] else 'Ping failed'))

            # eventually we will put code here that will log the actual output of self.nProcess.stdout to a log file


    def __nebulaStart(self, exe='', cFile='', cPath='') -> None:
        """
        private method to start nebula for threading

        :param exe       : path to nebula executable
        :type  exe       : string
        :param cFile: path to nebula config file
        :type  cFile: string
        :param cPath: path in which config file is located
        :type  cPath: string
        """
        # we only execute if these arguments are passed properly
        if exe == '' or cFile == '':
            return

        self.logger.debug('Starting nebula in separate thread')

        if cPath != '':
            os.chdir(cPath)

        self.nProcess = subprocess.Popen([exe, '-config', cFile])


    def __validateIp(self, ip) -> bool:
        """
        private function to validate an IP address.

        :param ip: IP address to validate
        :type  ip: string
        :returns : boolean denoting validity
        """
        reIpFour = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        reIpSix  = '^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$'

        if type(ip) == str:
            if re.match(reIpFour, ip) or re.match(reIpSix, ip):
                return True
            else:
                return False

        return False


    def connect(self) -> None:
        """
        runs the nebula binary

        :param configFile: full path to the config file
        :type  configFile: string
        """
        self.logger.info('Starting Nebula connection.')
        self.logger.debug(f'Keep alive: {self.keepAlive}, Use ping: {self.usePing}, pingInterval: {str(self.pingInterval)}, pingTargets: {str(self.pingTargets)}')
        nPathBase = os.path.dirname(__file__) + os.sep + 'bin' + os.sep + '{os}' + os.sep + '{exe}'
        showShell = True

        # load proper binary
        if sys.platform.startswith('darwin'):
            self.nPath = nPathBase.format(os='macos', exe='nebula')
        elif sys.platform.startswith('win32'):
            self.nPath = nPathBase.format(os='windows', exe='nebula.exe')
        else:
            return 
            # because this application does not work with Linux!

        if self.validConfig:
            self.connected = True

            if self.testMode:
                elevate()
                showShell = False
        
            # start Nebula connection
            exeThread = threading.Thread(target=self.__nebulaStart, kwargs={'exe': self.nPath, 'cFile': self.configFile, 'cPath': self.configPath})
            exeThread.start()

            # start connection checker
            checkThread = threading.Thread(target=self.__checkConnect)
            checkThread.daemon = True
            checkThread.start()
            
            self.logger.info(f'Nebula connection started with following credentials: executable={self.nPath}, configFile={self.configFile}')

        else:
            self.logger.error(f'Passed configuration file {self.configFile} was invalid.')

    def disconnect(self) -> None:
        """
        stops the nebula binary
        """
        self.logger.info('Disconnecting Nebula connection')
        if self.nProcess:
            self.connected = False
            self.threadEvent.set()
            try:
                os.kill(self.nProcess.pid, signal.SIGINT)
            except Exception as e:
                self.logger.info(f'Unable to kill nebula process: {e}; Continuing with regular disconnect.')
            self.nProcess = False


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

        if sys.platform.startswith('win32'):
            pingCommand = f"ping {ip} -n {count}"
        else:
            pingCommand = f"ping {ip} -c {count}"

        if self.__validateIp(ip):
            p = subprocess.Popen(pingCommand, stdout=subprocess.PIPE, encoding='utf-8', shell=True)

            for line in p.stdout:
                if 'TTL' in line or 'ttl' in line:  # Windows uses upper case; MacOS uses lowercase
                    result = True
                    data.append(line)

        return { 'result': result, 'output': data } if verbose else { 'result': result }


    def restartConnection(self) -> None:
        """
        Disconnects, then reconnects the connection after waiting 1.5 sec
        """
        if self.connected:
            self.logger.debug('Restarting Nebula connection.')

            # kill Nebula process
            try:
                os.kill(self.nProcess.pid, signal.SIGINT)
            except Exception as e:
                self.logger.info(f'Unable to kill nebula process: {e}; Continuing with regular restart.')
            self.nProcess = False
            
            # wait for reconnection
            sleep(1.5)

            # start Nebula process
            if self.validConfig:
                exeThread = threading.Thread(target=self.__nebulaStart, kwargs={'exe': self.nPath, 'cFile': self.configFile, 'cPath': self.configPath})
                exeThread.start()


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
                    self.pingTargets = config['lighthouse']['hosts']  # we ping the lighthouses to see if we're alive.
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

        if sys.platform.startswith('darwin'):
            nPath = nPathBase.format(os='macos', binary='nebula')
        elif sys.platform.startswith('win32'):
            nPath = nPathBase.format(os='windows', binary='nebula.exe')
        else:
            return False 
            # because this application does not work with Linux!

        out = []
        with subprocess.Popen([nPath, '-version'], stdout=subprocess.PIPE) as p:
            while p.poll() is None:
                out.append(p.stdout.read())
            return out[0].decode('utf-8')[9:-1]


if __name__ == '__main__':
    print("This module is not meant to be called by itself unless testing. Please import using from nebula import Nebula.")

    try:
        if sys.platform.startswith('darwin'):
            cf = ''
        elif sys.platform.startswith('win32'):
            cf = ''

        n = Nebula(cf, test=True)
        n.connect()
        sleep(10)
        n.disconnect()
        sleep(3)
        exit()
        # ips = ['192.168.3.1']

        # print(n.ping(ips[0], verbose=True))

    except SystemExit:
        pass


