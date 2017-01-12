# File System Tools

An assortment of scripts for quotidian uses.

### Issues:
+ [ ] copy_images.py
 - Source and target (ln 62-63) assume relative path rather than full path. If a full path is given, then no files will be copied.
 - On Windows fs, directories are marked with back-slash (`\`) instead of front-slash (`/`); therefore, users should note to use back-slashes or escaped back-slash (`\\`) when specifying target and source directories.
 - File paths that contain non-standard characters (e.g. downloaded web pages) will throw an error.

### TODO:
+ [ ] Resolve issues as mentioned above
+ [ ] Add docstrings
+ [ ] Ensure input is sanitized
+ [ ] Add unit tests

### License:
BSD-2 License. Copyright © 2016 Dee Reddy.
