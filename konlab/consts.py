"""
This module contains all the variables for konlab
"""
import os, pathlib


ROOT_DIR = pathlib.Path(__file__).parent.parent
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "default.yaml")
LOGS_FILE = os.path.join(CONFIG_DIR, "logs.log")
EXPORT_DIR = os.path.join(ROOT_DIR, "exports/")

#Setting this as "null" will not make archives out of the profiles but export it as a folder
EXPORT_FORMAT = "tar"

VERSION = "0.1"
