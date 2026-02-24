-Think of new values to be parsed in parse.py
-Update readme
-Think if I should fix naming error when exporting all profiles at the same time (export_name is ignored) --> 23/02/2026: Easiest fix will "dump" all profiles into a single file, which as of now I do not like, I want every profile to be kept separated.
-Specify where file logs are saved


DONES:
-export vs save --> export will only "save" when exporting a profile, save will also export but also save content to .config (meaning, export is backup, save is for version/file control) --> Done: Just export, profiles instead of being created dynamically are fields in the yamls
-unzip vs tar --> DONE: tar (with compression) is the best for linux environments
-main export_profile
-main reapply_profile
-test if i can input a subfolder or a file in a subfolder in the "files" option for an entry in a configuration file. --> As of 02/02/2026 Seems to work partially. If for example I have a location "test_location/" that contains folder "foo_folder", which in turn contains "foo" and "bar", I can set an entry as "foo_folder" and it will copy the whole folder, however, I cant copy individual items in the subfolder. Meaning that a given location can only SELECTIVELY copy all elements in it (and folders recursively).
-Should I package --> Not for the moment, keep all minimum code and config inside project and let users specify more config if they desire 
-Test what happens if I specify a file (instead of folder) in location --> 
    -(17/02/2026) When exporting and applying, both don't fail, just ignores entry.
-Allow specifying empty location and full path files in config --> Done, both for applying and exporting. If mixing full path file and non-empty location, file path takes precedence (due to how os.path.join prioritizes, there are no code baseguards so better not mix)
-Test export_all with multiple profiles and check if it properly works with and without setting export_name --> (2026/02/17) All good except exporting all profiles with custom name, as it will be ignored and export with profile name
-Add option to ensure removal of specific files when applying a profile