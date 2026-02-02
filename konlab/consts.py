"""
This module contains all the variables for konlab
"""
import os



HOME = os.path.expandvars("$HOME")
CONFIG_DIR = "" #"/home/zeus/Projects/Programacion/konlab/test_data/conf.yaml" #Force user to specify config
KONSAVE_DIR = "TODO: REmove"
CONFIG_FILE = CONFIG_DIR #TODO: Remove
LOGS_FILE = "logs.log" #TODO: In main.py pass parameter to LOGS
EXPORT_DIR = "test_data/exports/" #TODO: Change to something more "standard"

EXPORT_FORMAT = "tar" #Setting this as "null" will not make archives out of the profiles but export it as a folder

VERSION = "0.1"
