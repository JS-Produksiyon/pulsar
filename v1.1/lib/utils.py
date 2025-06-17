#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar_gui2.py
    Date Created: 2025-05-22
    Date Modified: 2025-06-17
    Python version: 3.11+
"""
__description__ = """
    Backend utilities for Pulsar.
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.1.0"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en']  # languages the interface has been translated into.
__debugState__ = True
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)
# ================================================================================
import sys, os, yaml, locale

# global variables
root_dir = os.path.dirname(os.path.dirname(__file__))

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
        settingsFile = root_dir + os.sep + 'settings.yaml'
        logFile = root_dir + os.sep + 'nebula.log'
    osLocale = locale.getdefaultlocale()

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
    settings = {'settings_version': __version__, 
                'language': osLocale[0],    # language code, e.g. 'en', 'fr', 'de'
                'tray_start': True,         # whether to start Pulsar in the system tray
                'keep_alive': True,         # whether to keep Nebula connection alive
                'use_ping': True,           # whether to use ping method to check Nebula connection; this is hard-coded for now
                'ping_interval': 300,       # ping interval in seconds
                'log_level': 'info',        # log level for Nebula (debug, info, warning, error, critical)
                'timestamp': '',            # timestamp of when the settings were last saved
                'nebula_log': logFile,      # path to the Nebula log file
                'display_mode': 'system',   # display mode for the GUI (system, light or dark)
                'profiles': [{              # list of Nebula profiles; for now max is 5
                                                # each profile is stored in a directory corresponding to the 
                                                # index of the profile in the list under the `profiles` directory
                    'name': 'Profile 1',        # profile name
                    'active': True,             # whether this profile is active
                    'remote_hosts': '',         # either hosts file or standard list of remote hosts in hosts format
                    'uses_hosts': False,        # whether this profile uses a hosts file
                    'auto_connect': False,      # whether to auto-connect this upon Pulsar start
                }], 
                'flask_settings': {         # Flask settings for the GUI web server 
                    'token': '',            # token for the Flask web server; empty for now
                },        
                'gui_port': 5000,            # port for the Flask web server to listen on
            }
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
        settingsFile = root_dir + os.sep + 'settings.yaml'

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
    scaffold = {'settings_version': str, 'language': str, 'tray_start': bool,  
                'keep_alive': bool, 'use_ping': bool, 'ping_interval': int, 
                'log_level': str, 'timestamp': str, 'nebula_log': str, 'display_mode': str, 
                'profiles': list, 'flask_settings': dict, 'gui_port': int}

    profile_scaffold = {'name': str, 'active': bool, 'remote_hosts': str,  
                        'uses_hosts': bool, 'auto_connect': bool}
    flask_scaffold = {'token': str}

    if type(settings) != dict:
        return False
    
    if len(settings.keys()) != len(scaffold.keys()):
        return False
    
    for k in settings.keys():
        if k not in scaffold.keys() or type(settings[k]) != scaffold[k]:
            return False

    if len(settings['language']) > 3:
        return False

    # check the profiles
    if len(settings['profiles'] > 0) and len(settings['profiles']) < 6:
        for profile in settings['profiles']:
            if type(profile) != dict:
                return False
            if len(profile.keys()) != len(profile_scaffold.keys()):
                return False
            for pk in profile.keys():
                if pk not in profile_scaffold.keys() or type(profile[pk]) != profile_scaffold[pk]:
                    return False
    else:
        return False
    
    # check the flask settings
    if len(settings['flask_settings'].keys()) != len(flask_scaffold.keys()):
        return False

    for fk in settings['flask_settings'].keys():
        if fk not in flask_scaffold.keys() or type(settings['flask_settings'][fk]) != flask_scaffold[fk]:
            return False

    return True


# General Utilities
def dark_mode():
    """
    Check if the system is in dark mode.

    :returns
    """
    dark_mode = False

    if sys.platform == "darwin":
        # macOS: use "defaults read -g AppleInterfaceStyle"
        try:
            import subprocess
            proc = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # If the command returns "Dark", then dark mode is enabled.
            dark_mode = (proc.returncode == 0 and proc.stdout.strip() == "Dark")
        except Exception as e:
            # In any error assume light mode.
            dark_mode = False

    elif sys.platform.startswith("win"):
        # Windows: use winreg to read "AppsUseLightTheme"
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key = winreg.OpenKey(registry, key_path)
            # The value: 0 means dark mode; 1 means light mode.
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            dark_mode = (value == 0)
        except Exception as e:
            # If any errors, default to light mode.
            dark_mode = False

    else:
        # For other platforms (e.g., various Linux desktop environments).
        # We assume dark mode as default.
        dark_mode = True

    return dark_mode


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
