from os import path, chdir
import sys


def configure_app_paths():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        chdir(sys._MEIPASS)

        if sys._MEIPASS not in sys.path:
            sys.path.insert(0, sys._MEIPASS)
    else:
        chdir(path.dirname(path.abspath(__file__)))
