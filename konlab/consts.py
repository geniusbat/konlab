"""
This module contains all the variables for konlab
"""
import os, shutil, pathlib


ROOT_DIR = pathlib.Path(__file__).parent.parent
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "default.yaml")
LOGS_FILE = os.path.join(CONFIG_DIR, "logs.log") #By default this will write into the same directory the script is run
EXPORT_DIR = os.path.join(ROOT_DIR, "exports/")

EXPORT_FORMAT = "tar" #Setting this as "null" will not make archives out of the profiles but export it as a folder

VERSION = "0.1"
