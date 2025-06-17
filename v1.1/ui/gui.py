#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: gui.py
    Date Created: 2025-06-17
    Date Modified: 2025-06-17
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

import sys

# Check for Python version
MIN_PYTHON = (3, 11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

import webview

class PulsarGuiApi:
    """
    This class provides the API for the Pulsar GUI to interact with the backend.
    It includes methods for handling various GUI-related tasks.
    """

    def __init__(self, window):
        self.window = window


class PulsarGui:
    """
    This class manages the Pulsar GUI using pywebview.
    It initializes the webview window and sets up the necessary API for interaction.
    """

    def __init__(self, config):
        self.config = config
        self.window = None
        self.api = PulsarGuiApi(self.window)

    def run(self):
        """
        Run the Pulsar GUI using pywebview.
        """
        # Create the webview window
        self.window = webview.create_window(
            'Pulsar',
            url='http://localhost:5000',  # Assuming Flask is running on this URL
            width=800,
            height=600,
            resizable=True,
            fullscreen=False,
            debug=True,
            js_api=self.api
        )
        
        # Start the webview event loop
        webview.start()