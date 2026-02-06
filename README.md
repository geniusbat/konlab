<h1 align=center> Konlab (Konlab for your homelab!) </h1>
<p align=center>A CLI program based on Konsave that is rather oriented towards creating backups in homelabs with dispersed files</p>

---

<p align="center">
    <img src="http://100.95.90.112:25555/image.png" alt="TestImage">
<img src="https://user-images.githubusercontent.com/39525869/109611033-a6732c80-7b53-11eb-9ece-ffd9cef49047.gif" />
</p> <!--TODO: Image from selfhosted nginx--> 

---

## Why Konlab? Why not just Konsave
<p>
    
</p>

---

## Roadmap

<i>Review "TODO.md" for a more up to date and shor-term oriented goals.</i>

- Add common placeholders
- Better file reapplying (I feel that if it fails there is no way back)
- Profile performance of modules
- Python package
- Maybe common backup configuration

---

## Installation 
<p>As of now the source code is available, everything it needs (module-wise) is self-contained in the project, therefore all you need is to download, install requirements and run main.py</p>
<p>Creating a python package will be added to the roadmap once the project reaches a certain maturity.</p>
<i>
  <p>
    Do note that the default config located at "config/default.yaml", isn't valid to start backing up your things.
    This is because every server and every user's needs are different and it would be very hard to come upon a generalized configuration. <br>
    Therefore use the mentioned config file as an example to create your own!
  </p>
</i>

## Usage
<p>These are the functionalities available in main.py</p>

### Get help
`-h` or `--help`

### Get version
`--version`

### Specify config file
`-c <config_file>` or `--config <config_file>` <br>
Specify what config to use for working with profiles. <br>

### List available profiles
`-l` or `--list`

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

## The configuration file

<p>
    The configuration file is the backbone to actually make Konlab usefull. By default (as of 03/02/2026) Konlab doesn't provide any configuration/profiles, I feel every user's needs are different and it would be hard to come upon a generalized configuration.
</p>
<p>
    Therefore it is imperative to design your own configuration to backup everything you need!
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
</p>

TODO: Explain functions

---

## Contributing
This is a very opinionated project that satisfies most of MY needs. As it uses Prayag2/konlab as upstream (https://github.com/Prayag2/konlab/), I would invite you to instead contribute to their awesome project as they sure do deserve the attention!

## License
This project uses GNU General Public License 3.0
