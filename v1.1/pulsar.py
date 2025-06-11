#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar.py
    Date Created: 2025-05-18
    Date Modified: 2025-06-10
    Python version: 3.11+
"""
__description__ = """
    This is the redesigned main process for the Pulsar application based on
    pywebview2 and pysystray.
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.3"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en']  # languages the interface has been translated into.
__nebula__ = 'decoupled'
__build__ = '2025-05-18 14:59'
__debugState__ = True
# ================================================================================
# Check for python version
import sys, os, locale

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

from PIL import Image
import pystray
from flask_babel import gettext as _
from lib.utils import dark_mode, loadSettings, touch
from ui.pulsar_ui import run_gui

# global variables
gui_windows = None
tray_icon = None
settings = None
icon_on = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1.png')) # tray icon when connected
if dark_mode():
    icon_off = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1-white.png'))
else:
    icon_off = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1-black.png'))

tray_menu_strings = {
    'connect': _('Connect to Nebula Network'),
    'disconnect': _('Disconnect from Nebula Network'),
    'window': _('Open Pulsar Window'),
    'exit': _('Exit Pulsar')
}

# Global functions
def shutdown():
    """
    Shuts down the Pulsar application gracefully.
    """
    global gui_windows, tray_icon
    tray_icon.stop()


def tray_click():
    """
    Handles the system tray icon click event.
    """
    global gui_windows


def connect():
    """ 
    Changes taskbar icon and executes connection to Nebula
    """
    global tray_icon
    tray_icon.icon = icon_on
    tray_icon.title = _('Pulsar is connected')


def disconnect():
    """
    Changes taskbar icon and executes disconnection from Nebula
    """
    global tray_icon
    tray_icon.icon = icon_off
    tray_icon.title = _('Pulsar is disconnected')


if __name__ == '__main__':
    # Start the Pulsar application
    # Load settings
    # Instantiate GUI windows
    # Check for first run; if so open first run dialog
    # instantiate system tray icon
    tray_menu = pystray.Menu(
        pystray.MenuItem(tray_menu_strings['connect'], connect),
        pystray.MenuItem(tray_menu_strings['disconnect'], disconnect), 
        pystray.Menu.SEPARATOR, 
        pystray.MenuItem(tray_menu_strings['window'], lambda: run_gui(), default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(tray_menu_strings['exit'], shutdown)
    )
    tray_icon = pystray.Icon(
        name='Pulsar',
        icon=icon_off,
        title=_('Pulsar is disconnected'),
        menu=tray_menu,
        on_click=tray_click
    )
    tray_icon.run()
