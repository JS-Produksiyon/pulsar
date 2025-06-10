#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar-ui.py
    Date Created: 2025-06-02
    Date Modified: 2025-06-10
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

import os
from jinja2 import Environment, FileSystemLoader
import webview
from flask import Flask, render_template
from lib.utils import dark_mode

# Flask app setup
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

# Babel setup (optional, placeholder for future localization)
from flask_babel import Babel, gettext as _
babel = Babel(app)

# Window configuration
winv = 512  # Window width
winh = 512  # Window height
maximize_button = True  # Toggle maximize button
display_mode = 'light' if dark_mode() else 'dark'  # Set display mode based on dark mode

# Jinja2 environment setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
env = Environment(loader=FileSystemLoader(template_dir))

@app.route('/')
def main():
    global display_mode
    # Render the main.html template
    return render_template('main.html.jinja', mode=display_mode)

# API 
class PulsarUiJsApi():
    """
    This class provides the API for the Pulsar UI to interact with the backend.
    It includes methods for handling dark mode, window management, and other UI-related tasks.
    """

    def exitApp(self):
        """
        Exit the application.
        """
        print("Exiting Pulsar UI...")
        webview.windows[0].destroy()


# activate GUI
def start_gui(dark_mode=False):
    """
    Starts the PyWebview GUI and Flask server.
    """
    # Set dark mode if enabled
    win_bkg = '#212529' if dark_mode else '#FFFFFF'

    print (win_bkg)

    # Start the Flask server in a separate thread
    from threading import Thread
    server_thread = Thread(target=lambda: app.run(debug=True, use_reloader=False))
    server_thread.daemon = True
    server_thread.start()

    # Path to the app icon
    icon_path = os.path.join(static_dir, 'img', 'pulsar-icon-1.1.png')

    # Start the PyWebview GUI
    webview.create_window(
        title=_("Pulsar : A GUI for Nebula"),
        url="http://localhost:5000/",
        width=winv,
        height=winh,
        resizable=maximize_button, 
        background_color=win_bkg,
        js_api=PulsarUiJsApi(),
        frameless=True
    )
    webview.start(icon=icon_path, debug=__debugState__)

# Expose the GUI functionality for external calls
def run_gui():
    """
    Entry point for external scripts to start the GUI.
    """
    print(dark_mode())
    start_gui(dark_mode=dark_mode())

if __name__ == "__main__":
    # Development entry point
    start_gui(dark_mode=dark_mode())

