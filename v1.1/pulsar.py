#!/user/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

# ================================================================================
"""
    File name: pulsar.py
    Date Created: 2025-05-18
    Date Modified: 2025-09-01
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
__version__ = "1.1.0"
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
# ================================================================================


import builtins
import pystray
from PIL import Image
from flask_babel import gettext as _
from lib.utils import dark_mode, loadSettings, touch

# forward reference Pulsar class for type hinting
builtins.pulsar: 'Pulsar'


# global Pulsar object
class Pulsar():
    """
    All globally necessary functions and values to be used with builtins
    Allows the Pulsar application to shut down gracefully, connect, disconnect,
    and change the 
    """

    def __init__(self, settings):
        self.gui_api = None
        self.gui_server:GuiServer
        self.gui_windows:PulsarGui
        self.tray_icon = None
        self.tray_menu = None
        self.settings = settings
        
        # initialize tray icon
        self.icon_on = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1.png')) # tray icon when connected
        if dark_mode():
            self.icon_off = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1-white.png'))
        else:
            self.icon_off = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui','static','img','pulsar-icon-1.1-black.png'))

        tray_menu_strings = {
            'connect': _('Connect to Nebula Network'),
            'disconnect': _('Disconnect from Nebula Network'),
            'window': _('Open Pulsar Window'),
            'exit': _('Exit Pulsar')
        }

        tray_menu = pystray.Menu(
            pystray.MenuItem(tray_menu_strings['connect'], self.connect),
            pystray.MenuItem(tray_menu_strings['disconnect'], self.disconnect), 
            pystray.Menu.SEPARATOR, 
            pystray.MenuItem(tray_menu_strings['window'], lambda: self.gui_windows.start(), default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(tray_menu_strings['exit'], self.shutdown)
        )

        self.tray_icon = pystray.Icon(
            name='Pulsar',
            icon=self.icon_off,
            title=_('Pulsar is disconnected'),
            menu=tray_menu,
            on_click=self.tray_click
        )

    def __str__(self):
        return f"<Pulsar Class. Current settings: {self.settings}>"

    # Global functions
    def shutdown(self):
        """
        Shuts down the Pulsar application gracefully.
        """
        self.gui_server.stop()   # type: ignore
        self.gui_windows.stop()  # type: ignore
        self.tray_icon.stop()    # type: ignore


    def tray_click(self):
        """
        Handles the system tray icon click event.
        """
        pass


    def connect(self, profile=0):
        """ 
        Changes taskbar icon and executes connection to Nebula
        :param profile: Index of profile to connect; 0 = all profiles (default)
        :type  profile: int
        """
        self.tray_icon.icon = self.icon_on                # type: ignore
        self.tray_icon.title = _('Pulsar is connected')   # type: ignore


    def disconnect(self, profile=0):
        """
        Changes taskbar icon and executes disconnection from Nebula
        :param profile: Index of profile to disconnect; 0 = all profiles (default)
        :type  profile: int
        """
        self.tray_icon.icon = self.icon_off                  # type: ignore
        self.tray_icon.title = _('Pulsar is disconnected')   # type: ignore

    def run_gui(self, app, host='127.0.0.1', port=5000):
        """
        Runs the Flask web server through waitress in a separate thread.
        :param app: Flask application instance.
        :param host: Host address for the Flask server.
        :param port: Port number for the Flask server.
        """
        #serve(app, host=host, port=port, threads=4, _quiet=True)
        app.run(host=host, port=port, debug=__debugState__, use_reloader=False)

# Start the Pulsar application
# Load settings
builtins.pulsar = Pulsar(loadSettings()) # type: ignore

# initialize these afterwards, so builtins has the pulsar object
from ui.webserver import GuiServer
from ui.gui import PulsarGui, PulsarGuiMainApi


if __name__ == '__main__':
    # Start the Flask web server
    builtins.pulsar.gui_server = GuiServer() 
    builtins.pulsar.gui_server.start()
    # Instantiate GUI windows
    builtins.pulsar.gui_windows = PulsarGui(dark_mode())
    if not builtins.pulsar.settings['tray_start']:
        builtins.pulsar.gui_windows.start()

    print(builtins.pulsar.gui_windows, builtins.pulsar.gui_server)


    # Check for first run; if so open first run dialog
    # instantiate system tray icon
    builtins.pulsar.tray_icon.run()
