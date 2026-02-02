-Change logging dir
-Think if I should have a default config in somewhere default as /etc/konlab or if to force user
-Think of new values to be parsed in parse.py
-Add option to ensure removal of specific files

DONES:
-export vs save --> export will only "save" when exporting a profile, save will also export but also save content to .config (meaning, export is backup, save is for version/file control) --> Done: Just export, profiles instead of being created dynamically are fields in the yamls
-unzip vs tar --> DONE: tar (with compression) is the best for linux environments
-main export_profile
-main reapply_profile
-test if i can input a subfolder or a file in a subfolder in the "files" option for an entry in a configuration file. --> As of 02/02/2026 Seems to work partially. If for example I have a location "test_location/" that contains folder "foo_folder", which in turn contains "foo" and "bar", I can set an entry as "foo_folder" and it will copy the whole folder, however, I cant copy individual items in the subfolder. Meaning that a given location can only SELECTIVELY copy all elements in it (and folders recursively).