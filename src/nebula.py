#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: nebula.py
    Date Created: 2024-05-03
    Date Modified: 2024-05-03
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

import os, subprocess
from pyuac import main_requires_admin

@main_requires_admin
def runNebula(configFile):
    """
    runs the nebula binary

    :param configFile: full path to the config file
    :type  configFile: string
    """
    nPath = os.path.dirname(__file__) + os.sep + 'bin' + os.sep + 'windows' + os.sep + 'nebula.exe'
    configPath = configFile[:configFile.rfind(os.sep)] if os.sep in configFile else ''
    if configPath != '':
        os.chdir(configPath)
    subprocess.Popen(f'{nPath} -config {configFile}', shell=True)
    input('pause')
    pass

if __name__ == '__main__':
    runNebula('C:\\Users\\wolfh\\Repositories\\pulsar\\creds\\joshw-config.yaml')