-test if i can input a subfolder or a file in a subfolder in the "files" option for an entry in a configuration file.
-Change logging dir
-Think if I should have a default config in somewhere default as /etc/konlab or if to force user
-Think of new values to be parsed in parse.py

DONES:
-export vs save --> export will only "save" when exporting a profile, save will also export but also save content to .config (meaning, export is backup, save is for version/file control) --> Done: Just export, profiles instead of being created dynamically are fields in the yamls
-unzip vs tar --> DONE: tar (with compression) is the best for linux environments
-main export_profile
-main reapply_profile