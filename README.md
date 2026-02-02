<h1 align=center> Konlab (Konlab for your homelab!) </h1>
<p align=center>A CLI program based on Konsave that is rather oriented towards creating backups in homelabs with dispersed files</p>

---

<p align="center">
<img src="https://user-images.githubusercontent.com/39525869/109611033-a6732c80-7b53-11eb-9ece-ffd9cef49047.gif" />
</p> <!--TODO: Image from selfhosted nginx--> 

---

## Installation 
<p>As of now the source code is available, everything it needs is selfcontained in the project, therefore all you need is to download, install requirements and run main.py</p>
<p>Creating a python will be added to the roadmap.</p>
<i>
  <p>
    Do note that the default config located at "config/default.yaml", isn't valid to start backing up your things.
    This is because every server and every user's needs are different and it would be very hard to come upon a generalized configuration. <br>
    Therefore use the mentioned config file as an example to create your own!
  </p>
</i>

## Differences to Konsave

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

## Roadmap

<i>Review "TODO.md" for a more up to date and shor-term oriented goals.</i>

- Add common placeholders
- Better file reapplying (I feel that if it fails there is no way back)
- Profile performance of modules
-

TODO:

TODO: Update with new guide

## Editing the configuration file
You can make changes to Konlab's configuration file according to your needs. The configuration file is located in `~/.config/konlab/conf.yaml`.
When using Konlab for the first time, you'll be prompted to enter your desktop environment.  
For KDE Plasma users, the configuration file will be pre-configured.

### Format
The configuration file should be formatted in the following way:
```yaml
---
save:
    name:
        location: "path/to/parent/directory"
        entries: 
        # These are files to be backed up.
        # They should be present in the specified location.
            - file1
            - file2
export:
    # This includes files which will be exported with your profile.
    # They will not be saved but only be exported and imported.
    # These may include files like complete icon packs and themes..
    name:
        location: "path/to/parent/directory"
        entries: 
            - file1
            - file2
...
```

### Adding more files/folders to backup
You can add more files/folders in the configuration file like this:
```yaml
save:
    name:
        location: "path/to/parent/directory"
        entries:
            - file1
            - file2
            - folder1
            - folder2
export:
    anotherName:
            location: "another/path/to/parent/directory"
            entries:
                - file1
                - file2
                - folder1
                - folder2
```

### Using placeholders
You can use a few placeholders in the `location` of each entry in the configuration file. These are:  
`$HOME`: the home directory  
`$CONFIG_DIR`: refers to "$HOME/.config/"  
`$SHARE_DIR`: refers to "$HOME/.local/share"  
`$BIN_DIR`: refers to "$HOME/.local/bin"  
`${ENDS_WITH="text"}`: for folders with different names on different computers whose names end with the same thing.  
The best example for this is the ".default-release" folder of firefox.  
`${BEGINS_WITH="text"}`: for folders with different names on different computers whose names start with the same thing.  


```yaml
save:
    firefox:
        location: "$HOME/.mozilla/firefox/${ENDS_WITH='.default-release'}"
        entries:
            - chrome
```

---

## Contributing
This is a very opinionated project that satisfies most of MY needs. As it uses Prayag2/konlab as upstream (https://github.com/Prayag2/konlab/), I would invite you to instead contribute to their awesome project as they sure do deserve the attention!

## License
This project uses GNU General Public License 3.0
