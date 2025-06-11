#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar-ui.py
    Date Created: 2025-06-10
    Date Modified: 2025-06-10
    Python version: 3.11+
"""
__description__ = """
    This segment provides the api necessary for pywebview to interact with the back end
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

