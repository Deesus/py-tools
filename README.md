# File System Tools

An assortment of scripts for quotidian uses.

### Issues:
+ [ ] update_xml_attributes.py
- Make script/operation more object-oriented
- Modularize update_xml_attributes so that user can call class functions rather than having to edit script itself

+ [ ] copy_images.py
 - The print out of the number of files copied can be wrong; the count includes overriden files (i.e. same names), among others, that doesn't reflect the actual end state of copied files.
 - Source and target (ln 62-63) assume relative path rather than full path. If a full path is given, then no files will be copied.
 - On Windows fs, directories are marked with back-slash (`\`) instead of front-slash (`/`); therefore, users should note to use back-slashes or escaped back-slash (`\\`) when specifying target and source directories.
 - File paths that contain non-standard characters (e.g. downloaded web pages) will throw an error.

### TODO:
+ [ ] Resolve issues as mentioned above
+ [ ] Add docstrings
+ [ ] Ensure input is sanitized
+ [ ] Add unit tests

### License:
BSD-2 License. Copyright © 2016-2017 Dee Reddy.
