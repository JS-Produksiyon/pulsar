#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: utils.py
    Date Created: 2024-05-06
    Date Modified: 2024-06-27
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.2"
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

import os, yaml
from pathlib import Path
from PySide6.QtCore import QCoreApplication, QLocale, QTranslator, QLibraryInfo
from PySide6.QtWidgets import QMessageBox, QApplication

# Dialogs
def errModal(parent,msg,errList=[],endMsg="") -> None:
    """
    Displays a modal with an error message and optionally a list of generated errors
    
    :param parent  : reference to calling QMainWindow class
    :type  parent  : QMainWindow
    :param msg     : Message to display
    :type  msg     : string
    :param errList : List of errors to display as unordered list
    :type  errList : list
    :param endMsg  : a message to display after the list or in a second paragraph.
    :type  endMsg  : string
    """
    errOut = "<html><head/><body><p>{msg}</p>{list}{closing}</body></html>"
    errListOut = ""
    errListItems = ""

    # generate list of errors
    if type(errList) == list and len(errList) > 0:
        for e in errList:
            errListItems += "<li>{}</li>".format(e)
        errListOut = "<ul>{}</ul>".format(errListItems)
    
    if endMsg != "":
        endMsg = "<p>{}</p>".format(endMsg)

    # concatenate error message to display
    box = QMessageBox.critical(parent, parent.tr("Pulsar - Error!"), 
            errOut.format(msg=msg,list=errListOut,closing=endMsg))


def infoModal(parent, msg) -> None:
    """
    Pops up an informational modal
    
    :param parent  : reference to calling QMainWindow class
    :type  parent  : QMainWindow
    :param msg     : Message to display
    :type  msg     : string
    """
    msgOut = "<html><head/><body><p>{msg}</p></body></html>"

    box = QMessageBox.information(parent, parent.tr("Pulsar"), 
                                  msgOut.format(msg=msg))


def yesNoModal(parent, msg) -> bool:
    """
    Pops up an informational modal
    
    :param parent  : reference to calling QMainWindow class
    :type  parent  : QMainWindow
    :param msg     : Message to display
    :type  msg     : string
    """
    msgOut = "<html><head/><body><p>{msg}</p></body></html>"

    box = QMessageBox.question(parent, parent.tr("Pulsar"),
                                msgOut.format(msg=msg))

    if box == QMessageBox.Yes:
        return True
    else:
        return False

# General functions
def timestamp() -> str:
    """
    creates a timestamp of right now in YYYY-mm-ddThh:mm:ssZ±hh:00 format
    """
    import time, pytz
    from datetime import datetime
    from tzlocal import get_localzone
    
    localTz = get_localzone()
    timeStamp = time.time()
    utc_now = datetime.fromtimestamp(timeStamp)
    local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(localTz)
    return local_now.strftime('%Y-%m-%dT%H:%M:%SZ%z')


# Settings functions
def loadSettings() -> dict:
    """
    loads the settings file from disk or else generates the settings dictionary

    :returns: dict
    """
    if sys.platform == 'darwin':
        settingsFile = os.environ.get('HOME') + '/Library/Application Support/Pulsar/settings.yaml'
        logFile = os.environ.get('HOME') + '/Library/Application Support/Pulsar/nebula.log'
        touch(os.environ.get('HOME') + '/Library/Application Support/Pulsar', dir=True)
        touch(logFile)
    else:
        settingsFile = os.path.dirname(__file__) + os.sep + 'settings.yaml'
        logFile = './nebula.log'
    locale = QLocale()

    if os.path.exists(settingsFile):
        with open(settingsFile, 'r', encoding='utf-8') as file:
            settings = yaml.safe_load(file)

        if validateSettings(settings):
            # make sure we don't have macos_elevate as True if we're not running MacOS
            if not sys.platform.startswith('darwin'):
                settings['macos_elevate'] = False            
            # here we return the valid settings object
            return settings

    # we ALWAYS return a clean settings object, even if there is an error in the file, which will automatically
    # overwrite the corrupt settings.yaml file (if possible). This way Pulsar should always start, simply 
    # displaying a "set up your settings file" dialog if necessary.
    settings = {'settings_version': __version__,'config': '', 'language': locale.languageToCode(locale.language()),
            'tray_start': True, 'auto_connect': False, 'keep_alive': True, 'use_hosts': False, 'hosts_file': '', 
            'use_ping': True, 'ping_interval': 300, 'log_level': 'info', 'timestamp': '', 'nebula_log': logFile, 
            'macos_elevate': False}
    saveSettings(settings)
    return settings


def saveSettings(settings) -> bool:
    """
    saves the passed settings dict to the settings yaml file

    :param settings: settings dictionary to save
    :type  settings: dict
    :returns       : boolean denoting validity
    """
    settings['timestamp'] = timestamp()


    # we can only use_hosts if we have a valid hosts_file
    if settings['hosts_file'] == '':
        settings['use_hosts'] = False

    if sys.platform == 'darwin':
        settingsFile = os.environ.get('HOME') + '/Library/Application Support/Pulsar/settings.yaml'
    else:
        settingsFile = os.path.dirname(__file__) + os.sep + 'settings.yaml'

    try:
        with open(settingsFile, 'w', encoding='utf-8') as file:
            yaml.dump(settings, file)
        return True
    except:
        return False


def touch(filename, dir=False) -> bool:
    """
    Checks to see if the passed filename or directory exists. 
    If not, creates the file as an empty file or attempts to make the directory.
    
    :param filename: Name of file to check
    :type  filename: string
    :param dir     : whether we are touching a directory
    :type  dir     : boolean
    :returns       : boolean denoting success
    """
    if dir == True:
        try:
            if not os.path.exists(filename):
                os.mkdir(filename)
        except Exception as e:
            print(f'Unable to create directory {filename}: {e}')
            return False

    else:
        if not os.path.exists(filename):
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    pass
            except Exception as e:
                print(f'Unable to create file {filename}: {e}')
                return False
    
    return True

def validateSettings(settings) -> bool:
    """
    validates the settings dictionary
    
    :param settings: settings dictionary to save
    :type  settings: dict
    :returns       : boolean denoting validity
    """
    scaffold = {'settings_version': str, 'config': str, 'language': str, 'tray_start': bool, 'auto_connect': bool, 
                'keep_alive': bool, 'use_hosts': bool, 'hosts_file': str, 'ping_interval': int, 'use_ping': bool, 
                'log_level': str, 'timestamp': str, 'nebula_log': str, 'macos_elevate': bool}

    if type(settings) != dict:
        return False
    
    if len(settings.keys()) != len(scaffold.keys()):
        return False
    
    for k in settings.keys():
        if k not in scaffold.keys() or type(settings[k]) != scaffold[k]:
            return False

    if len(settings['config']) > 0 and not os.path.exists(settings['config']):
        return False

    if len(settings['language']) > 3:
        return False

    return True


if __name__ == '__main__':
    print('This module is not meant to be used in a standalone manner. Please call it using import utils.')
    print(timestamp())