#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: utils.py
    Date Created: 2024-05-06
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

import os, yaml
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

# Settings functions
def loadSettings() -> dict:
    """
    loads the settings file from disk or else generates the settings dictionary

    :returns: dict
    """
    settingsFile = os.path.dirname(__file__) + os.sep + 'settings.yaml'
    locale = QLocale()

    if os.path.exists(settingsFile):
        with open(settingsFile, 'r', encoding='utf-8') as file:
            settings = yaml.safe_load(file)

        if validateSettings(settings):
            return settings
        else:
            return False
        
    else:
        settings = {'config': '', 'language': locale.languageToCode(locale.language()),
             'tray_start': True, 'auto_connect': False, 'use_hosts': False, 'hosts_file': ''}
        saveSettings(settings)
        return settings


def saveSettings(settings) -> bool:
    """
    saves the passed settings dict to the settings yaml file

    :param settings: settings dictionary to save
    :type  settings: dict
    :returns       : boolean denoting validity
    """
    # we can only use_hosts if we have a valid hosts_file
    if settings['hosts_file'] == '':
        settings['use_hosts'] = False

    settingsFile = os.path.dirname(__file__) + os.sep + 'settings.yaml'

    try:
        with open(settingsFile, 'w', encoding='utf-8') as file:
            yaml.dump(settings, file)
        return True
    except:
        return False


def validateSettings(settings) -> bool:
    """
    validates the settings dictionary
    
    :param settings: settings dictionary to save
    :type  settings: dict
    :returns       : boolean denoting validity
    """
    scaffold = {'config': str, 'language': str, 'tray_start': bool, 'auto_connect': bool, 'use_hosts': bool, 'hosts_file': str}

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
    settings = loadSettings()
    print(settings)