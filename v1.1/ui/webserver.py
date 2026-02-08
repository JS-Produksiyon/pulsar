#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: webserver.py
    Date Created: 2025-06-17
    Date Modified: 2025-06-20
    Python version: 3.11+
"""
__description__ = """
    The flask app that serves the Pulsar GUI.
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
# ================================================================================
import os
import builtins
import threading
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect
from flask_babel import Babel, gettext as _
from lib.utils import random_string

class GuiServer():

    def __init__(self):
        """
        Initialize the GUIServer with the given builtins.pulsar.settings.
        :param builtins.pulsar.settings: builtins.pulsar.settings object or dictionary.
        """
        self.app = None
        self.thread = None


    def __str__(self) -> str:
        return f'<GuiServer Class - Manages the web server that serves up the pages in pywebview>'
        

    # Main Flask application
    def create_app(self) -> Flask:
        """
        Create a Flask application instance with the given builtins.pulsar.settingsuration.
        :return      : Flask application instance.
        """

        app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

        # set secret token
        token = builtins.pulsar.settings['flask_settings']['token']

        # Load babel for internationalization
        app.config['BABEL_DEFAULT_LOCALE'] = builtins.pulsar.settings['language']
        app.config['BABEL_SUPPORTED_LOCALES'] = __languages__
        app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.dirname(__file__), 'translations')
        babel = Babel(app)

        # set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        env = Environment(loader=FileSystemLoader(template_dir))

        # Set the locale selector for Babel
        @babel.localeselector
        def get_locale():
            # Dynamically select the best match for the user's language
            if builtins.pulsar.settings['language'] not in app.config:
                return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
            else:
                return builtins.pulsar.settings['language']
        

        # make sure that we only allow the webserver to be accessed by pywebview
        @app.before_request
        def before_request():
            """
            Prevent any host but pywebview from accessing the Flask server
            """
            remote_token = request.headers.get('X-PulsarGUI-Token') or request.args.get('pulsargui_token')
            
            if not __debugState__ and remote_token != token:
                return redirect('https://github.com/JS-Produksiyon/pulsar/wiki', 302) 


        # Define routes
        @app.route('/')
        def main():
            """
            Render the main page of the Pulsar GUI.
            """
            return render_template('main.html.jinja', mode=builtins.pulsar.settings['display_mode']) 

        @app.route('/about')
        def about():
            """
            Render the about page of the Pulsar GUI.
            """
            return render_template('about.html.jinja', mode=builtins.pulsar.settings['display_mode'], version=builtins.pulsar.settings['version'])


        @app.route('/first-run')
        def first_run():
            """
            Render the first run setup page of the Pulsar GUI.
            """
            return render_template('first-run.html.jinja', mode=builtins.pulsar.settings['display_mode'], settings=builtins.pulsar.settings)


        @app.route('/settings')
        def settings():
            """
            Render the settings page of the Pulsar GUI.
            """
            return render_template('settings.html.jinja', mode=builtins.pulsar.settings['display_mode'], settings=builtins.pulsar.settings)
        

        @app.route('/settings/profile/<int:id>')
        def profile(id):
            """
            Render the profile page for a specific Nebula connection profile.
            This page should ONLY be called from the Profiles tab on the settings page.    
            :param id: The numeric ID of the profile to display.
            """
            if id < 0 or id >= len(builtins.pulsar.settings['profiles']):
                return redirect('/settings', 302)
            
            # code to retrieve profile data based on id

            return render_template('profile.html.jinja', mode=builtins.pulsar.settings['display_mode'])


        return app


    def start(self) -> None:
        """
        Start the Flask web server with the given builtins.pulsar.settingsuration.
        Mostly to be used with threading.
        :param builtins.pulsar.settings: builtins.pulsar.settingsuration object or dictionary.
        :type  builtins.pulsar.settings: dict
        :return      : None
        """
        self.app = self.create_app()
        self.thread = threading.Thread(
            target=self.app.run,
            kwargs={'use_reloader':False, 'debug':False}, 
            daemon=True)
        self.thread.start()


    def stop(self) -> None:
        """
        Stop the Flask web server.
        This method should be called to gracefully shut down the server.
        :return: None
        """
        if self.thread is not None and self.thread.is_alive():
            self.thread = None


if __name__ == '__main__':
    app = GuiServer()
    app.start()
