#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: gui.py
    Date Created: 2025-06-17
    Date Modified: 2025-06-20
    Python version: 3.11+
"""
__description__ = """
    This is the segment that handles serving up the GUI using pywebview.
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

import multiprocessing.process
import sys

# Check for Python version
MIN_PYTHON = (3, 11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)
# ================================================================================

import time
import multiprocessing        # required for webview per https://pywebview.flowrl.com/examples/pystray_icon.html
import webview
from flask_babel import gettext as _
import builtins

class PulsarGuiMainApi():
    """
    This class provides the API for the Pulsar GUI to interact with the backend.
    It includes methods for handling various GUI-related tasks.
    """
    def __init__(self) -> None:
        self.shutdown_cmd = builtins.pulsar.shutdown

    def __str__(self) -> str:
        return f'<PulsarGuiMainApi Class - Used to connect with pywebview main window front end functions>'

    def exitApp(self) -> None:
        """
        Trigger Shutdown of Pulsar
        """
        if self.shutdown_cmd:
            print (builtins.pulsar)
            print (builtins.pulsar.gui_server)
            pass
            #self.shutdown_cmd()


    def nebulaConnect(self, profile=0):
        """
        Trigger Nebula connection
        :param profile: Index of profile to connect; 0 = all profiles (default)
        :type  profile: int
        """
        if self.connect_callback:
            self.connect_callback()

    def nebulaDisconnect(self, profile=0):
        """
        Disconnect Nebula connection
        :param profile: Index of profile to disconnect; 0 = all profiles (default)
        :type  profile: int
        """
        if self.disconnect_callback:
            self.disconnect_callback(profile)        


class PulsarGuiSecondaryApi():
    """
    Secondary window JavaScript API frontend connections
    """
    def __init__(self):
        pass

    def __str__(self) -> str:
        return f'<PulsarGuiMainApi Class - Used to connect with pywebview secondary window front end functions>'


class PulsarGui():
    """
    This class manages the Pulsar GUI using pywebview.
    It initializes the webview window and sets up the necessary API for interaction.
    """

    def __init__(self, dark_mode=True):
        print(builtins.pulsar)
        print(builtins.pulsar.gui_server)
        if sys.platform == 'darwin':
            ctx = multiprocessing.get_context('span')
            self.Process = ctx.Process
            self.Queue = ctx.Queue
        else:
            self.Process = multiprocessing.Process
            self.Queue = multiprocessing.Queue

        self.webview_process = None

        self.url = f"http://localhost:{pulsar.settings['gui_port']}/"

        if builtins.pulsar.settings['display_mode'] == 'system':
            self.win_bkg = '#212529' if dark_mode else '#FFFFFF'
        else:
            self.win_bkg = '#FFFFFF' if pulsar.settings['display_mode'] == 'light' else '#212529'
            # we ALWAYS default to dark mode!


    def __str__(self) -> str:
        return f'<PulsarGui Class - Drives pywebview windows>'
      

    def open_main_window(self, command_queue=None) -> None:
        """
        Opens the main Pulsar window using pywebview.
        """
        windows = {}
        api = {'main': PulsarGuiMainApi(), 'secondary': PulsarGuiSecondaryApi()}

        # set up only the main window
        windows['main'] = webview.create_window(
                'Pulsar',
                url=self.url,  # Assuming Flask is running on this URL
                width=512,
                height=512,
                resizable=False,
                fullscreen=False,
                frameless = True,
                easy_drag= True,
                background_color=self.win_bkg,
                js_api=api['main'],
            )
        
        def create_secondary(loc):
            pages = {
                'about': {'title': _('About Pulsar'), 'path': 'about'},
                'first-run': {'title': 'Pulsar: ' + _('Set Up Application'), 'path': 'first-run'},
                'settings': {'title': 'Pulsar: ' + _('Settings'), 'path': 'settings'}
            }
            if loc in pages and 'secondary' not in windows:
                windows['secondary'] = webview.create_window(
                    pages[loc]['title'],
                    url=f"{self.url}{pages[loc]['path']}",
                    height=768,
                    width=1024,
                    resizable=True,
                    fullscreen=False,
                    debug=__debugState__,
                    background_color=self.win_bkg,
                    js_api=api['secondary'],
                )

        def interface():
            """
            Send commands to the webview thread
            """
            while True:
                if command_queue:
                    if not command_queue.empty():
                        cmd = command_queue.get()
                        if cmd == 'destroy_main' and 'main' in windows:
                            windows['main'].destroy()
                            del windows['main']
                        elif cmd == 'destroy_secondary' and 'secondary' in windows:
                            windows['secondary'].destroy()
                            del windows['secondary']
                        elif cmd == 'destroy_all':
                            # Destroy all windows
                            for win in list(windows.values()):
                                win.destroy()
                            windows.clear()
                            break
                        elif cmd.startswith('open_secondary:'):
                            # e.g., 'open_secondary:settings'
                            _, loc = cmd.split(':', 1)
                            create_secondary(loc)
                time.sleep(0.1)

        import threading
        threading.Thread(target=interface, daemon=True).start()

        webview.start(debug=__debugState__)


    def start(self) -> None:
        """
        Starts the Pulsar GUI.
        This method should be called to initialize and run the GUI.
        """
        if self.webview_process is None or not self.webview_process.is_alive():
            self.command_queue = self.Queue()
            self.webview_process = self.Process(target=self.open_main_window, args=(self.command_queue,))
            self.webview_process.start()


    def stop(self) -> None:
        """
        Stops the Pulsar GUI.
        This method should be called to close the GUI and clean up resources.
        """
        if self.webview_process is not None and self.webview_process.is_alive():
            self.command_queue.put('destroy_all')
            self.webview_process.join(timeout=5)
            if self.webview_process.is_alive():
                self.webview_process.terminate()
