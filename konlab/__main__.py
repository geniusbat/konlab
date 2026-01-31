"""Konlab entry point."""

import argparse
import os
import shutil
from konlab import funcs
from konlab.consts import (
    VERSION,
    CONFIG_DIR,
    EXPORT_DIR
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
        help="Export a specific profiles",
        metavar="<name>",
    )
    parser.add_argument(
        "--export-all",
        required=False,
        help="Export all profiles",
        action="store_true",
    )
    parser.add_argument( #TODO: Make force the default
        "-d",
        "--dry-run",
        required=False,
        action="store_true",
        help="Just test, do not actually backup anything",
    )
    parser.add_argument(
        "-z", "--compress", 
        required=False, 
        action="store_true", 
        help="Add if desiring to compress output when exporting a profile"
    )
    parser.add_argument( #TODO: Think if needed
        "-n",
        "--export-name",
        required=False,
        help="Specify the export name when exporting a profile",
        metavar="<archive-name>"
    )
    parser.add_argument(
        "-v", "--version", required=False, action="store_true", help="Show version"
    )

    return parser


def main():
    """The main function that handles all the arguments and options."""

    config = funcs.read_konlab_config(CONFIG_DIR)
    assert not config is None, f"Configuration doesn't seem to be valid or is empty, check {CONFIG_DIR}"

    funcs.log(f"Loaded config: {CONFIG_DIR}")
    parser = _get_parser()
    args = parser.parse_args()

    if args.list:
        funcs.list_profiles(config)
    elif args.print:
        profile = funcs.get_profile(config, args.print)
        print(profile)
    elif args.export_all:
        #TODO
        pass
    elif args.export_profile:
        #TODO: Expport function
        funcs.export(config=config,
            dry_run=args.dry_run, 
            profile_name=args.export_profile, 
            export_directory=EXPORT_DIR, 
            #export_name=args.export_name, 
            compress=args.compress, 
        )
    elif args.version:
        print(f"Konlab: {VERSION}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
