"""
This module contains all the variables for konlab
"""
import os
from konlab import __version__


HOME = os.path.expandvars("$HOME")
CONFIG_DIR = "/home/zeus/Projects/Programacion/konlab/test_data/conf.yaml" #TODO: In main.py make it so I can pass different conf paths
SHARE_DIR = os.path.join(HOME, ".local/share") #TODO: Remove
BIN_DIR = os.path.join(HOME, ".local/bin") #TODO: Remove
KONSAVE_DIR = "TODO: REmove"
CONFIG_FILE = CONFIG_DIR #TODO: Remove
LOGS_FILE = "/home/zeus/Projects/Programacion/konlab/test_data/logs.log" #TODO: In main.py pass parameter to LOGS
EXPORT_DIR = "/home/zeus/Projects/Programacion/konlab/test_data/exports/"

EXPORT_FORMAT = "tar"

VERSION = __version__
