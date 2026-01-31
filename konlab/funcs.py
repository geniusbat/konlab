"""
This module contains all the functions for konlab.
"""

import os
import shutil
import traceback
from datetime import datetime
from zipfile import is_zipfile, ZipFile
from konlab.consts import (
    HOME,
    CONFIG_FILE,
    EXPORT_FORMAT,
    LOGS_FILE
)
from konlab.parse import TOKEN_SYMBOL, tokens, parse_functions, parse_keywords

try:
    import yaml
except ModuleNotFoundError as error:
    raise ModuleNotFoundError(
        "Please install the module PyYAML using pip: \n pip install PyYAML"
    ) from error


def exception_handler(func):
    """Handles errors, prints nicely and logs into file. #TODO: Logging

    Args:
        func: any function

    Returns:
        Returns function
    """

    def inner_func(*args, **kwargs):
        try:
            function = func(*args, **kwargs)
        except Exception as err:
            dateandtime = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

            with open(LOGS_FILE, "a", encoding="utf-8") as file:
                file.write(dateandtime + "\n")
                traceback.print_exc(file=file)
                file.write("\n")

            print(
                f"ERROR: {err}\nPlease check the log at {LOGS_FILE} for more details."
            )
            return None

        return function

    return inner_func


def mkdir(path):
    """Creates directory if it doesn't exist.

    Args:
        path: path to the new directory

    Returns:
        path: the same path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def log(msg, *args, **kwargs):
    """Logs text.

    Args:
        msg: the text to be printed
        *args: any arguments for the function print()
        **kwargs: any keyword arguments for the function print()
    """
    with open(LOGS_FILE, "a", encoding="utf-8") as file:
        dateandtime = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        file.write(dateandtime+" "+msg)
        file.write("\n")
    print(f"Konlab: {msg}", *args, **kwargs)


@exception_handler
def copy(source, dest):
    """
    This function was created because shutil.copytree gives error if the destination folder
    exists and the argument "dirs_exist_ok" was introduced only after python 3.8.
    This restricts people with python 3.7 or less from using Konlab.
    This function will let people with python 3.7 or less use Konlab without any issues.
    It uses recursion to copy files and folders from "source" to "dest"

    Args:
        source: the source destination
        dest: the destination to copy the file/folder to
    """
    assert isinstance(source, str) and isinstance(dest, str), "Invalid path"
    assert source != dest, "Source and destination can't be same"
    assert os.path.exists(source), "Source path doesn't exist"

    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(source_path):
            copy(source_path, dest_path)
        else:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            if os.path.exists(source_path):
                shutil.copy(source_path, dest)


@exception_handler
def read_konlab_config(config_file) -> dict:
    """Reads config_file and parses it.

    Args:
        config_file: path to the config file
    """
    with open(config_file, "r", encoding="utf-8") as text:
        konlab_config = yaml.load(text.read(), Loader=yaml.SafeLoader)
    parse_keywords(tokens, TOKEN_SYMBOL, konlab_config)
    parse_functions(tokens, TOKEN_SYMBOL, konlab_config)

    # in some cases conf.yaml may contain nothing in "entries". Yaml parses
    # these as NoneType which are not iterable which throws an exception
    # we can convert all None-Entries into empty lists recursively so they
    # are simply skipped in loops later on
    def convert_none_to_empty_list(data):
        if isinstance(data, list):
            data[:] = [convert_none_to_empty_list(i) for i in data]
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = convert_none_to_empty_list(v)
        return [] if data is None else data

    return convert_none_to_empty_list(konlab_config)

@exception_handler
def list_profiles(data:dict):
    """Lists all the available profiles.
    """

    assert len(data) != 0, "No profiles found."

    # run
    print("Konlab profiles:")
    print("ID\tNAME")
    profiles = list(data.keys())
    for i in range(len(profiles)):
        profile = profiles[i]
        print(f"{i + 1}\t{profile}")


@exception_handler
def get_profile(config:dict, profile_name:str):
    """Get profile data
    """

    assert len(config) != 0, "No profiles found."
    assert profile_name in config.keys(), "Profile not found in given config."

    return config[profile_name]


@exception_handler
def export(config:dict, dry_run:bool, profile_name:str, export_directory:str, export_name:str=None, compress:bool=False):#profile_name, profile_list, profile_count, archive_dir, archive_name, force):
    """It will export the specified profile as a ".knsv" to the specified directory.
       If there is no specified directory, the directory is set to the current working directory.

    Args:
        TODO: Add args
    """

    #TODO: Dry-run

    # assert
    assert os.path.exists(export_directory), f"Export path given '{export_directory}' does not exist."
    assert profile_name in config.keys(), f"No profile {profile_name} found in given config {config}."

    if export_name is None:
        export_name = profile_name

    #File copying function for later
    def aux_copy(source, dest):
        if os.path.exists(source):
            if os.path.isdir(source):
                copy(source, dest)
            else:
                shutil.copy(source, dest)
        else:
            log(f"Given {source} wasn't valid")

    # run
    full_export_path = os.path.join(export_directory, export_name)

    #Create full_export_path directory if needed
    mkdir(full_export_path)
        
    log(f"Starting export of profile {profile_name} to {full_export_path}")

    
    profile_data = get_profile(config, profile_name)

    for entry_name in profile_data.keys():
        entry = profile_data[entry_name]
        import_location = entry["location"]
        #Get export path for given entry and create folder if needed
        entry_export_path = os.path.join(full_export_path, entry_name)
        mkdir(entry_export_path)
        log(f"For entry {entry_name}:")
        #Check if first element of "files" for given entry is "__all__", in that case copy all files in the given import_location
        if len(entry["files"])>0 and entry["files"][0] == "__all__":
            log(f'Exporting all files...')
            if not dry_run:
                aux_copy(
                    import_location,
                    os.path.join(entry_export_path)
                )
        else:
            #If not, import specificly given files
            for file in entry["files"]:
                source = os.path.join(import_location, file)
                dest = os.path.join(entry_export_path, file)
                log(f'Exporting "{file}"...')
                if not dry_run:
                    aux_copy(source, dest)

    #Also backup the config file used, so later I can reuse it if needed
    shutil.copy(CONFIG_FILE, full_export_path)

    log("Creating archive")
    #TODO: Compress
    archive_format = EXPORT_FORMAT
    if not dry_run:
        #If desiring to compress then change format to one with compression
        if compress:
            if archive_format == "tar":
                archive_format = "gztar"
            else:
                archive_format = "zip"
                log(f"Could not find compress format for {EXPORT_FORMAT}")
        shutil.make_archive(base_name=full_export_path, format=archive_format, root_dir=export_directory)

    #Delete temporal export directory as archive was created
    shutil.rmtree(full_export_path)

    log(f"Successfully exported to {full_export_path}.{archive_format}")
