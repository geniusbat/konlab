<h1 align=center> Konlab (Konsave for your homelab!) </h1>
<p align=center>A CLI program based on Konsave that is rather oriented towards creating backups in homelabs with dispersed files</p>

---

## Why Konlab? Why not just Konsave?
<p>
    Konlab  is a CLI program used to manage backups of config files in homelab environments where configuration files are scattered across the system. Thus, Konlab can be used to unify and archive configurations for the various applications in use.
</p>
<p>
    Konsave is an amazing tool to quickly play around and export/import configurations, however, I felt the main goal was to cover desktop environments, and though it can be used to backup anything you might need,
    I felt it was lacking on some "niceties" when making backups (ie: compression and custom export directories, deleting files) while having unnecessary functionalities (ie: locally saving profiles). 
</p>
<p>
    Konlab's goal is to be as simple on its config as possible to let the user transparently define the expected behaviour. In Konsave most of the configuration needed to work is stored in the file "consts.py", while Konlab expects the user to define everything when executing the program.
</p>

### Nomenclature

- Profile: Set of configuration files.
- Config file: Yaml file defining a set of profiles. 
- Export: Synonym to backup, basicallly take all the files defined for a profile in a config file and coppy/save them to a different location and archive it. 
- Applying: Moving the files back from an exported archive to its origin. 

---

## Roadmap

<i>Review "TODO.md" for a more up to date and shor-term oriented goals.</i>

- Add common placeholders
- Better file reapplying (I feel that if it fails there is no way back)
- Profile performance of modules
- Python package
- Exporting to remote servers

---

## Installation 
<p>As of now the source code is available, everything it needs (module-wise) is self-contained in the project, therefore all you need is to download, install requirements.txt and run main.py</p>
<p>
    The next step would be creating a yaml file with the configuration for backing up files. 
</p>
<i>
  <p>
    Do note that the default config located at "config/default.yaml", isn't valid to start backing up your things.
    This is because every server and every user's needs are different and it would be very hard to come upon a generalized configuration. <br>
    Therefore use the mentioned config file as an example to create your own!
  </p>
</i>

## Usage
<p>
    These are the functions when executing main.py
</p>

### Basic commands
| Command | Description | Example |
|---------|-------------|---------|
| `-h, --help` | Get help | `python main.y --help` |
| `--version` | Get version | `python main.y --version` |
| `-c, --config-file` | Specify config file to use | `python main.py -c <config_file>` |

<i>A valid config file containing profiles in yaml format must be given to use Konlab any further.</i>

### List available profiles
| Command | Description | Example |
|---------|-------------|---------|
| `-l, --list` | List available profiles given a valid yaml config file | `python main.y -c <config_file> --list` |

### Print profile data
`-p <profile_name>` or `--print <profile_name>` <br>
Where <profile_name> is the profile_name available inside the configuration being used. <br>

### Export profile
`-e <profile_name>` or `--export-profile <profile_name>` <br>
Export the profile <profile_name> available inside the configuration being used. <br>
#### Some optional parameters:
- `-d <export_path>` or `--directory <export_path>` <br>
Specify the location where the data will be exported. By default it goes to ./exports/ . <br>
- `-n <export_name>` or `--export-name <export_name>` <br>
Specify the name of the folder/archive in which the data will be exported. By default uses the profile name. <br>
- `-z` or `--compress` <br>
If using a valid format (meaning that it can be compressed, ie: zips and tars) creates a compressed archive. By default compression is not enabled <br>
- `-f <format>` or `--format <format>` <br>
Specify the name of the folder/archive in which the data will be exported. By default uses tar. <br>
- `--dry-run` <br>
Run as test, meaning that no actual files will be copied, useful to preventively detect errors. <br>
- `-v` or `--verbose` <br>
Set how verbose the script should run, depends on how many v are added (0:info only to console, 1: debug only to console, 2: debug to console and info to file, 3: write everything to file and console) <br>

### Export all available profiles in configuration
`-export-all`
Export all available profiles for configuration being used.
#### Some optional parameters:
- `-d <export_path>` or `--directory <export_path>` <br>
Specify the location where the data will be exported. By default it goes to ./exports/ . <br>
- `-n <export_name>` or `--export-name <export_name>` <br>
Specify the name of the folder/archive in which the data will be exported. By default uses the profile name. <br>
- `-z` or `--compress` <br>
If using a valid format (meaning that it can be compressed, ie: zips and tars) creates a compressed archive. By default compression is not enabled <br>
- `-f <format>` or `--format <format>` <br>
Specify the name of the folder/archive in which the data will be exported. By default uses tar. <br>
- `--dry-run` <br>
Run as test, meaning that no actual files will be copied, useful to preventively detect errors. <br>
- `-v` or `--verbose` <br>
Set how verbose the script should run, depends on how many v are added (0:info only to console, 1: debug only to console, 2: debug to console and info to file, 3: write everything to file and console) <br>

### Reapply profile 
`-a <profile_name>` or `--reapply-profile <profile_name>` <br>
Reapply profile (meaning to automatically get files of the profile, given a configuration and backup directory, to the appropiate locations). <br>
#### Some optional parameters: 
- `-d <backup_path>` or `--directory <backup_path>` <br>
Specify the location where backup data is located. <br>
- `-d <temporal_directory>` or `--directory <temporal_directory>` <br>
Specify where to  hold profile files for reapplying a profile, folder doesn't need to exist as script will create it. By default /tmp is used. <br>
- `--no-clear` <br>
Do not remove temporal directory after reapplying profile. <br>
- `--dry-run` <br>
Run as test, meaning that no actual files will be copied, useful to preventively detect errors. <br>
- `-v` or `--verbose` <br>
Set how verbose the script should run, depends on how many v are added (0:info only to console, 1: debug only to console, 2: debug to console and info to file, 3: write everything to file and console) <br>

---

## The yaml configuration file

<p>
    The configuration file is the backbone to actually make Konlab usefull. By default (as of 03/02/2026) Konlab doesn't provide any configuration/profiles, I feel every user's needs are different and it would be hard to come upon a generalized configuration.
</p>
<p>
    Therefore it is imperative to design your own configuration to backup everything you need!
</p>
<p>
    A config file is a yaml containing profiles.
</p>

<p>
    In Konlab everything revolves around the profiles, defined in a configuration file. A profile is a set entries defining a location/directorie and the files inside it, that are to be backed up.
    This would be the format for a profile: <br>
    `
    profile_name:
        entry_name_A:
            location: "/path_to_foobaar" 
            files:
                - "foo"
                - "bar"
            delete:
                - "extra"
    `
    Where "profile_name" and "entry_name_A" are user-defined names. Meanwhile, "location" specifies the directory to be used for the entry, 
    "files" is a yaml array of filenames (assumed to be contained in "location"), which will be saved/copied when backing up "profile_name". <br>
    It is possible to specify a subfolder of "location" in "files", meaning that the folder (and all its contents, recursively) will be copied, it isn't possible to specify a file in a subfolder. Ie:
    #### Valid 
    `
    profile_name:
        entry_name_A:
            location: "/path_to_foobaar" 
            files:
                - "subfolder_inside_path"
    `
    This will copy /path/subfolder_inside_path.
    #### Invalid
    `
    profile_name:
        entry_name_A:
            location: "/path_to_foobaar" 
            files:
                - "subfolder_inside_path/file_inside"
    `
    Doing so will look for a file/folder named "subfolder_inside_path/item_inside" (escaping "/"). If desiring to copy only a specific file in a subfolder it is recommended to create another entry. Ie:
    `
    profile_name:
        entry_name_A:
            location: "/path_to_foobaar" 
            files:
                - "foo"
        entry_name_B:
            location: "/path_to_foobaar/subfolder_inside_path" 
            files:
                - "file_inside"
    `

    #### Using "__all__"
    <p>
        If the first element of the "files" array is "__all__" it will skip the subsequent definitions and instead copy all the contents inside "location".
    </p>
    #### Delete files when applying entry
    profile_name:
        entry_name_A:
            location: "/path_to_foobaar" 
            files:
                - "foo"
                - "bar"
            delete:
                - "extra"
    `
    <p>
        By using "delete" you can specify files/folders in "location" to be automatically deleted when applying a profile. 
    </p>
</p>


## Known errors
- -Applying a profile where the location doesn't exist will stop any further execution but will keep "pasted" previously copied files.
- -Exporting all profiles ("export-all" option) will ignore "named-export".

---

## Contributing
This is a very opinionated project that satisfies most of MY needs. As it uses Prayag2/konlab as upstream (https://github.com/Prayag2/konlab/), I would invite you to instead contribute to their awesome project as they sure do deserve the attention!

## License
This project uses GNU General Public License 3.0
