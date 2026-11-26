from __future__ import annotations

import os
import sys

# Anki imports
from aqt import gui_hooks, mw
from aqt.qt import QAction
from aqt.utils import qconnect, showInfo

ADDON_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(ADDON_DIR, "vendor")

if VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)


def _open_analyzer() -> None:
    try:
        from .gui import open_analyzer_dialog
    except ImportError:
        showInfo("DuDu 读度 dialog is not implemented yet.")
        return

    open_analyzer_dialog()


def _setup_menu() -> None:
    if mw is None:
        return

    action = QAction("DuDu 读度: Analyze Text", mw) # Create a clickable menu item
    qconnect(action.triggered, _open_analyzer) # Define what happens when the menu item is clicked
    mw.form.menuTools.addAction(action) # Insert the menu item at the end of the Tools menu


gui_hooks.main_window_did_init.append(_setup_menu)