"""Konlab entry point."""

import argparse, os, shutil
import logging, logging.config
from konlab import funcs
from konlab.consts import (
    VERSION,
    CONFIG_DIR,
    EXPORT_DIR,
    LOGS_FILE,
)

def _get_parser() -> argparse.ArgumentParser:
    """Returns CLI parser.

    Returns:
        argparse.ArgumentParser: Created parser.
    """
    parser = argparse.ArgumentParser(
        prog="Konlab",
        epilog="Please report bugs at TODO:Add url to repo",
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        type=str,
        help=f"Use a specific config file instead of the default at {CONFIG_DIR}",
        metavar="<config-path>",
    )
    parser.add_argument(
        "-l",
        "--list",
        required=False,
        help="List existing profiles",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--print",
        required=False,
        help="Print specific profile",
        type=str,
        metavar="<profile_name>",
    )
    parser.add_argument(
        "-e",
        "--export-profile",
        required=False,
        type=str,
        help="Export a specific profile",
        metavar="<name>",
    )
    parser.add_argument(
        "--export-all",
        required=False,
        help="Export all profiles",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--reapply-profile",
        required=False,
        type=str,
        help="Reapplies a specific profile to the necessary locations, it requirest to be given the backup file to use (-d)",
        metavar="<name>",
    )
    parser.add_argument(
        "--no-clear",
        required=False,
        help="If using --reapply-profile, tells it to not delete temporal directory used to reapply files",
        action="store_true",
    )
    parser.add_argument(
        "-z", "--compress", 
        required=False, 
        action="store_true", 
        help="Add if desiring to compress output when exporting a profile"
    )
    parser.add_argument(
        "-f",
        "--format",
        required=False,
        help="Specify the format type when archiving an exported profile, if set to null it will export is a folder",
        metavar="<format-name>"
    )
    parser.add_argument(
        "-d",
        "--directory",
        required=False,
        help="Specify where to export or get backup data to reapply profile",
        metavar="<export-path>"
    )
    parser.add_argument(
        "-n",
        "--export-name",
        required=False,
        help="Specify the export name when exporting a profile",
        metavar="<archive-name>"
    )
    parser.add_argument( #TODO: Make force the default
        "--dry-run",
        required=False,
        action="store_true",
        help="Just test, do not actually backup anything",
    )
    parser.add_argument(
        "-v", "--version", required=False, action="store_true", help="Show version"
    )
    return parser


LOG_CONFIG = {
        "version": 1,
        "formatters": {
            "standard": { 
                "format": "%(asctime)s [%(levelname)s]: %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"{LOGS_FILE}.default",
                "mode": "a",
                "maxBytes": 1048576,
                "backupCount": 4
            }
        },
        "loggers": {
            "": {  # root logger, all other loggers will be of this logger level implicitlly.
                "level":"DEBUG",
                "handlers": ["console", "file"], 
            },
        }
    }

def _configure_logger() -> None:
    logging.config.dictConfig(LOG_CONFIG)

def main():
    """The main function that handles all the arguments and options."""
    #Get arguments
    parser = _get_parser()
    args = parser.parse_args()

    _configure_logger()
    logger = logging.getLogger()

    #Get config to use, default to CONFIG_DIR
    use_config = CONFIG_DIR
    if args.config:
        assert os.path.exists(args.config), f"Config doesn't seem to exist at {args.config}"
        use_config = args.config
    
    config = funcs.read_konlab_config(use_config) #TODO: Dynamic config with option -c --config
    assert not config is None, f"Configuration doesn't seem to be valid or is empty, check {CONFIG_DIR}"

    logger.debug(f"Loaded config: {use_config}")

    #Extract auxiliary "directory" argument
    use_directory = EXPORT_DIR
    if args.directory:
        use_directory = args.directory
        assert os.path.exists(use_directory), "directory {use_directory} doesn't exist or isn't valid"
    
    #Extract format argument
    archive_format = ""
    if args.format:
        archive_format = args.format

    if args.list:
        funcs.list_profiles(config)
    elif args.print:
        profile = funcs.get_profile(config, args.print)
        print(profile)
    elif args.export_all:
        profile_names = config.keys()
        for name in profile_names:
            funcs.export(config=config,
                dry_run=args.dry_run, 
                profile_name=name, 
                export_directory=use_directory, 
                export_name=name, 
                compress=args.compress, 
                archive_format= archive_format,
            )
    elif args.export_profile:
        funcs.export(config=config,
            dry_run=args.dry_run, 
            profile_name=args.export_profile,
            export_directory=use_directory,
            export_name=args.export_name,
            compress=args.compress,
            archive_format= archive_format,
        )
    elif args.reapply_profile:
        assert len(use_directory)>0, "ERROR: directory option is empty"
        funcs.reapply_export(
            config=config,
            dry_run=args.dry_run, 
            profile_name=args.reapply_profile, 
            backup_file_dir=use_directory,
            temporal_dir="/home/zeus/Projects/Programacion/konlab/test_data/test_applying", #TODO: Dynamic
            delete_at_end=not args.no_clear
        )
    elif args.version:
        print(f"Konlab: {VERSION}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
