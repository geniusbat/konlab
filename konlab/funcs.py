"""
This module contains all the functions for konlab.
"""

import os, sys, shutil, traceback, logging
from datetime import datetime
from zipfile import is_zipfile, ZipFile
from consts import (
    EXPORT_FORMAT,
    LOGS_FILE
)
from parse import TOKEN_SYMBOL, tokens, parse_functions, parse_keywords

try:
    import yaml
except ModuleNotFoundError as error:
    raise ModuleNotFoundError(
        "Please install the module PyYAML using pip: \n pip install PyYAML"
    ) from error

#Get root logger
logger = logging.getLogger()

def exception_handler(func):
    """Handles errors, prints nicely and logs into file.

    Args:
        func: any function

    Returns:
        Returns function
    """

    def inner_func(*args, **kwargs):
        try:
            function = func(*args, **kwargs)
        except Exception as err:
            exc_info = (type(err), err, err.__traceback__)
            logger.error("Exception raised when running funcs.py", exc_info=exc_info)
            return None

        return function

    return inner_func


def mkdir(path) -> str:
    """Creates directory if it doesn't exist.

    Args:
        path: path to the new directory

    Returns:
        path: the same path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


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
def list_profiles(data:dict) -> None:
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
def get_profile(config:dict, profile_name:str) -> None:
    """Get profile data
    """

    assert len(config) != 0, "No profiles found."
    assert profile_name in config.keys(), "Profile not found in given config."

    return config[profile_name]


@exception_handler
def export(config:dict, dry_run:bool, profile_name:str, export_directory:str, export_name:str=None,config_path:str="", compress:bool=False, archive_format:str="") -> None:
    """It will export the specified profile as a ".knsv" to the specified directory.
       If there is no specified directory, the directory is set to the current working directory.
    """


    # assert
    assert os.path.exists(export_directory), f"Export path given '{export_directory}' does not exist."
    assert profile_name in config.keys(), f"No profile {profile_name} found in given config {config}."


    # prepare to run
    if export_name is None or len(export_name)==0:
        export_name = profile_name

    #Get archive format to use, remember that setting it to null will not actually archive but keep it as a folder
    if len(archive_format)==0:
        archive_format = EXPORT_FORMAT
    #Make sure archive_format (except for null) is valid
    if archive_format!="null":
        available_formats = [el[0] for el in shutil.get_archive_formats()]
        if not archive_format in available_formats:
            raise UserWarning(f"Specified format {archive_format} isn't valid, ensure it is in the following list: {available_formats}")


    #File copying function for later
    def aux_copy(source, dest):
        if os.path.exists(source):
            if os.path.isdir(source):
                copy(source, dest)
            else:
                shutil.copy(source, dest)
        else:
            logger.error(f"Given source {source} doesn't exist")


    # run
    full_export_path = os.path.join(export_directory, export_name)

    #Check if full_export_path exists and isn't empty, in that case instead of using it add some unique identifier to not override the contents
    #Skip if archive_format is null as it is expected that the user wants to override the contents. This is just a safeguard to not delete previous folder after archiving
    if os.path.exists(full_export_path) and len(os.listdir(full_export_path))>0 and archive_format != "null":
        new_path = full_export_path+datetime.now().strftime("%d%m%Y_%H%M%S")
        logger.warning(f"{full_export_path} doesn't seem to be empty, instead moving to the new path: {new_path}")
        full_export_path = new_path

    #Create full_export_path directory if needed
    mkdir(full_export_path)
    logger.info(f"Starting export of profile {profile_name} to {full_export_path}")
    
    profile_data = get_profile(config, profile_name)
    #Main loop to export files
    for entry_name in profile_data.keys():
        entry = profile_data[entry_name]
        import_location = entry["location"]
        #Get export path for given entry and create folder if needed
        entry_export_path = os.path.join(full_export_path, entry_name)
        mkdir(entry_export_path)
        logger.debug(f"For entry {entry_name}:")
        #Check if first element of "files" for given entry is "__all__", in that case copy all files in the given import_location
        if len(entry["files"])>0 and entry["files"][0] == "__all__":
            logger.debug(f'Exporting all files...')
            if not dry_run:
                aux_copy(
                    import_location,
                    os.path.join(entry_export_path)
                )
            #Just testing, make sure import_location exists
            else:
                if not os.path.exists(import_location):
                    logger.error(f"{import_location} doesn't exists, continuing with dry-run")

        else:
            #If not, import specificly given files
            for file in entry["files"]:
                source = os.path.join(import_location, file)
                #If file was given as an absolute path, only keep the filename
                if os.path.isabs(file):
                    file = os.path.splitext(os.path.basename(file))[0]
                dest = os.path.join(entry_export_path, file)
                logger.debug(f'Exporting "{file}"...')
                if not dry_run:
                    aux_copy(source, dest)
                #Just testing, make sure import_location exists
                else:
                    if not os.path.exists(source):
                        logger.error(f"{source} doesn't exists, continuing with dry-run")

    #Also backup the config used, so later I can reuse it if needed
    if not dry_run:
        if len(config_path)==0:
            logger.debug("Skip copying config file as none was given")
        elif not os.path.exists(config_path):
            logger.debug(f"Skip copying config file as it doesn't seem to exist: {config_path}")
        else:
            shutil.copy(config_path, full_export_path)

    if not dry_run and len(os.listdir(full_export_path))==0:
        logger.warning(f"WARNING: {full_export_path} seems to be empty! Proceeding anyways")
    
    #Create archive file 
    if not dry_run and archive_format!="null":
        logger.info("Creating archive")
        #If desiring to compress then change format to one with compression
        if compress:
            if archive_format == "tar":
                archive_format = "gztar"
            else:
                archive_format = "zip"
                logger.warning(f"Could not find compress format for {EXPORT_FORMAT}, using zip as default")
        base_name = os.path.join(export_directory, export_name)
        shutil.make_archive(base_name=base_name, format=archive_format, root_dir=full_export_path)

    #Delete temporal export directory (only if archive was created)
    if archive_format!="null":
        shutil.rmtree(full_export_path)


    pretty_full_export_path = os.path.join(export_directory, export_name)+"."+archive_format if archive_format != "null" else os.path.join(export_directory, export_name)

    if dry_run:

        logger.info(f"Dry-run completed to {pretty_full_export_path}, check previous errors")
    else:
        logger.info(f"Successfully exported to {pretty_full_export_path}")


@exception_handler
def reapply_export(config:dict, dry_run:bool, backup_file_dir:str, profile_name:str, temporal_dir:str, delete_at_end:bool=True) -> None:
    """
    Given a config and backup_file (that was generated from running "export") (the backup file can be an archive or an extracted directory from the file) reapply those files found inside for the given profile_name
    """

    # assert
    assert os.path.exists(backup_file_dir), f"Path of file/dir '{backup_file_dir}' does not exist."
    assert profile_name in config.keys(), f"No profile {profile_name} found in given config {config}."


    #File copying function for later
    def aux_copy(source, dest):
        if os.path.exists(source):
            if os.path.isdir(source):
                copy(source, dest)
            else:
                shutil.copy(source, dest)
        else:
            logger.error(f"aux_copy: Given source {source} doesn't exist")

    #Used for temporal_dir to ensure it is using an empty directory
    def warn_if_dir_exists(dir:str, only_rename=False) -> str:
        if os.path.exists(dir) and len(os.listdir(dir))>0:
            new_path = dir+datetime.now().strftime("%d%m%Y_%H%M%S")
            if not only_rename:
                logger.warning(f"{dir} doesn't seem to be empty, instead moving to the new path: {new_path}")
            return new_path
        return dir

    # run
    logger.info(f"Preparing to reapply config for {profile_name} from backup")

    #If no temporal_dir was given default to /tmp
    if len(temporal_dir)==0:
        temporal_dir = warn_if_dir_exists("/tmp/", True) #/tmp already exists therefore function will return an unique folder inside it
        logger.info(f"No temporal_dir was given, using {temporal_dir}")
    #Keep a copy of temporal_dir as it will be later be reasigned
    aux_temporal_dir = temporal_dir

    #Check if given backup_file_dir is a directory or an archive and copy contents to temporal_dir
    if os.path.isdir(backup_file_dir):
        logger.debug(f"{backup_file_dir} is a directory")
        #Copy folder to temporal_dir
        last_folder = os.path.basename(backup_file_dir)
        temporal_dir = os.path.join(temporal_dir, last_folder)
        mkdir(temporal_dir)
        copy(backup_file_dir, temporal_dir)
    #If it is a file, try to extract it, if it fails it may be an invalid file
    else:
        logger.debug(f"{backup_file_dir} is a file, extracting it")
        filename = os.path.splitext(os.path.basename(backup_file_dir))[0]
        temporal_dir = warn_if_dir_exists(temporal_dir)
        temporal_dir = os.path.join(temporal_dir, filename)
        #Unpack file to temporal_dir
        shutil.unpack_archive(backup_file_dir, temporal_dir)
    #Work on moving files in temporal_dir to the corresponding locations
    logger.info("Starting to apply profile files to corresponding locations")
    profile_data = get_profile(config, profile_name)
    for entry_name in profile_data.keys():
        entry = profile_data[entry_name]
        apply_to_location = entry["location"]
        files = entry["files"]
        #Check if first element of files is "__all__", if so copy all files
        if len(files)>0 and files[0] == "__all__":
            source = os.path.join(temporal_dir, entry_name)
            dest = os.path.join(apply_to_location)
            logger.debug(f'Applying all files...')
            if not dry_run:
                aux_copy(source, dest)
            #Just testing, make sure apply_to_location and file exists and
            else:
                if not os.path.exists(source):
                    logger.error(f"{file} at {source} does not exist in backup file")
                if not os.path.exists(apply_to_location):
                    logger.error(f"{apply_to_location} doesn't exists, continuing with dry-run")
        #If not just copy specified files in config
        else:
            for file in files:
                dest = os.path.join(apply_to_location, file)
                #If file was given as an absolute path, only keep the filename, 
                #it is assumed that if it comes as an absolute path then location is empty, thus "dest" must be defined before removing full path from file
                if os.path.isabs(file):
                    file = os.path.splitext(os.path.basename(file))[0]
                source = os.path.join(temporal_dir, entry_name, file)
                logger.debug(f'Applying "{file}"...')
                if not dry_run:
                    aux_copy(source, dest)
                #Just testing, make sure apply_to_location and file exists and
                else:
                    if not os.path.exists(source):
                        logger.error(f"{file} at {source} does not exist in backup file")
                    if not os.path.exists(apply_to_location):
                        logger.error(f"{apply_to_location} doesn't exists, continuing with dry-run")

    if dry_run or delete_at_end:
        logger.info(f"Deleting temporal directory: {aux_temporal_dir}")
        shutil.rmtree(aux_temporal_dir)
    else:
        logger.debug(f"Did not remove temporal directory: {aux_temporal_dir}")

    if dry_run:
        logger.info(f"Dry-run completed, check previous errors")
    else:
        logger.info(f"Remember that reapplying exports doesn't ensure the correct user/group permissions, specially if zip files, ensure that permissions are correct")
