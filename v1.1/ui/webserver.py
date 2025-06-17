#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: webserver.py
    Date Created: 2025-06-17
    Date Modified: 2025-06-17
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

import os
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect
from flask_babel import Babel, gettext as _

# Main Flask application
def create_app(config) -> Flask:
    """
    Create a Flask application instance with the given configuration.
    :param config: Configuration object or dictionary.
    :return      : Flask application instance.
    """

    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

    # set secret token
    token = config['flask_settings']['token']

    # Load babel for internationalization
    app.config['BABEL_DEFAULT_LOCALE'] = config['language']
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
        if config['language'] not in app.config:
            return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
        else:
            return config['language']
    

    # make sure that we only allow the webserver to be accessed by pywebview
    @app.before_request
    def before_request():
        """
        Prevent any host but pywebview from accessing the Flask server
        """
        if __debugState__:
            return True

        remote_token = request.headers.get('X-PulsarGUI-Token') or request.args.get('pulsargui_token')
        
        if remote_token != token:
                return redirect('https://github.com/JS-Produksiyon/pulsar/wiki', 302) 


    # Define routes
    @app.route('/')
    def main():
        """
        Render the main page of the Pulsar GUI.
        """
        return render_template('main.html.jinja', mode=config['display_mode']) 

    @app.route('/about')
    def about():
        """
        Render the about page of the Pulsar GUI.
        """
        return render_template('about.html.jinja', mode=config['display_mode'], version=config['version'])


    @app.route('/first-run')
    def first_run():
        """
        Render the first run setup page of the Pulsar GUI.
        """
        return render_template('first-run.html.jinja', mode=config['display_mode'], settings=config)


    @app.route('/profile/<id:int>')
    def profile(id: int):
        """
        Render the profile page for a specific Nebula connection profile.
        :param id: The numeric ID of the profile to display.
        """
        if id < 0 or id >= len(config['profiles']):
            return redirect('/settings', 302)
        
        # code to retrieve profile data based on id

        return render_template('profile.html.jinja', mode=config['display_mode'])


    @app.route('/settings')
    def settings():
        """
        Render the settings page of the Pulsar GUI.
        """
        return render_template('settings.html.jinja', mode=config['display_mode'], settings=config)
    

    
    return app
