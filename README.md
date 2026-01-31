<h1 align=center> Konlab (Konlab for your homelab!) </h1>
<p align=center>A CLI program based on Konlab that is rather oriented on 
 that will let you save and apply your Linux customizations with just one command! Konlab also lets you share your dot files to your friends in an instant! It officially supports KDE Plasma but it can be used on all other desktop environments too!</p>

---

<p align="center">
<img src="https://user-images.githubusercontent.com/39525869/109611033-a6732c80-7b53-11eb-9ece-ffd9cef49047.gif" />
</p>

---

## Installation -- TODO: Review
Install from PyPI using pip  
`python -m pip install konlab`

Install from PyPI using pipx  
`pipx install konlab`

## Usage 
### Get Help
`konlab -h` or `konlab --help`
### Save current configuration as a profile
`konlab -s <profile name>` or `konlab --save <profile name>`
### Overwrite an already saved profile
`konlab -s <profile name> -f` or `konlab -s <profile name> --force `
### List all profiles
`konlab -l` or `konlab --list`
### Remove a profile
`konlab -r <profile name>` or `konlab --remove <profile name>`
### Apply a profile
`konlab -a <profile name>` or `konlab --apply <profile name>`
You may need to log out and log in to see all the changes.  
### Export a profile as a ".knsv" file to share it with your friends!
`konlab -e <profile name>` or `konlab --export-profile <profile name>`
### Export a profile, setting the output dir and archive name
`konlab -e <profile name> -d <archive directory> -n <archive name>`
or
`konlab --export-profile <profile name> --archive-directory <archive directory> --export-name <export name>`
### Export a profile, overwrite files if they already exist
`konlab -e <profile name> -f` or `konlab --export-profile <profile name> --force`
*note: without --force, the export will be appended with the date and time to ensure unique naming and no data is overwritten
### Import a ".knsv" file
`konlab -i <path to the file>` or `konlab --import-profile <path to the file>`
### Show current version
`konlab -v` or `konlab --version`  
### Wipe all profiles
`konlab -w` or `konlab --wipe`

  
---


## Old from previous README: TODO: Update with new guide

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
This is a very opinionated project that satisfies most of MY needs. As it uses Prayag2/konlab as upstream (https://github.com/Prayag2/konlab/) I think any effort will be much appreciated there.

## License
This project uses GNU General Public License 3.0
