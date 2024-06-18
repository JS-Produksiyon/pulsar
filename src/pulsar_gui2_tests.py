#!/user/bin/env python
# -*- coding: utf-8 -*-
# This file is used to test certain PyQt functionality to see if I can make it work for 1.1

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication

app = QApplication([])  # Initialize the application
style_hints = QGuiApplication.styleHints()  # Get the style hints
print(f"Current style theme: {style_hints.colorScheme()}")
