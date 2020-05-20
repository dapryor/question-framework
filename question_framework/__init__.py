import importlib
import os
import sys
from os.path import basename

from . import package, post_process, question, user_input, validation



class add_path:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


def _load_all_modules_from_dir(dirname):
    directories = [basename(f.path) for f in os.scandir(dirname) if
                   f.is_dir() and not (basename(f.path).startswith("__") or basename(f.path).startswith("."))]
    with add_path(dirname):
        for name in directories:
            importlib.import_module(name, package=basename(dirname))


try:
    _load_all_modules_from_dir(os.environ["CONFIG_TOOL_PACKAGE_DIR"])
except KeyError:
    print("CONFIG_TOOL_PACKAGE_DIR environment variable not defined.")
    exit(1)

try:
    os.environ["CONFIG_TOOL_OUTPUT_DIR"]
except KeyError:
    print("CONFIG_TOOL_OUTPUT_DIR environment variable not defined.")
    exit(1)
