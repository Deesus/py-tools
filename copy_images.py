import os
import shutil
from optparse import OptionParser

""" Copies images from source to destination.

    Usage: python copy_images.py SOURCE TARGET [OPTIONS]

    Options:
        `largest-per-folder`: copies largest image for each folder and sub-folder.
        `smallest-per-folder`: copies smallest image for each folder and sub-folder.
"""

ALLOWED_FILES = frozenset({"jpg", "jpeg", "gif", "ico", "png"})


def commandline_options():
    # TODO: complete docstring
    """

    :return:
    """

    # Instantiate and add parser options:
    parser = OptionParser(usage="%prog [OPTIONS] FILENAME",
                          version="%prog 1.0")

    parser.add_option("-l",
                      "--largest-per-folder",
                      action="store_true",
                      help="Copies largest image for each folder and sub-folder.")

    parser.add_option("-s",
                      "--smallest-per-folder",
                      action="store_true",
                      help="Copies smallest image for each folder and sub-folder.")

    # TODO: Add/override default help option.

    # Parse options:
    (options, args) = parser.parse_args()

    # Call main function:
    main(args[0], args[1], options)


def main(source, target, command_options):
    # TODO: complete docstring
    """
    :param source:
    :param target:
    :param command_options:
    :return:
    """

    # TODO: Ensure interface can handle back-slash input as source/target -- i.e. trim slashes:
    source = "./" + source + "/"
    target = "./" + target + "/"

    files_to_copy = []

    for dir_, subdirs_, files_ in os.walk(source):
        # -----------------------------------------------
        # For each dir_, filter for only image files:

        # lambda checks file types of the file name
        filtered_files = list(filter(lambda file_: file_.split(".")[1] in ALLOWED_FILES, files_))

        # -----------------------------------------------
        # Ensure the full file path of the files:
        filtered_files_full_path = [dir_ + "/" + file_ for file_ in filtered_files]

        # -----------------------------------------------
        # Apply custom filter option (e.g. 'copy only largest file per folder', etc.):
        try:
            # For each dir_, add only the largest image for copying:
            if command_options.largest_per_folder:
                largest_file = max(filtered_files_full_path, key=lambda file_: os.stat(file_).st_size)
                files_to_copy.append(largest_file)

            # For each dir_, add only the smallest image for copying:
            elif command_options.smallest_per_folder:
                largest_file = min(filtered_files_full_path, key=lambda file_: os.stat(file_).st_size)
                files_to_copy.append(largest_file)

            # If no custom filter present, add all images for copying:
            else:
                files_to_copy.extend(filtered_files_full_path)
        except ValueError as e:
            pass

    # -----------------------------------------------
    # Copy files to target:
    try:
        [shutil.copy2(file_, target) for file_ in files_to_copy]
    except Exception as e:
        print("Unexpected error whilst copying -- ", e)

    # Printout:
    num_of_files = len(files_to_copy)
    print("Copied {} {}".format(num_of_files,
                                (num_of_files == 1 and "file") or "files")
          )

##############################
#           Main             #
##############################

if __name__ == "__main__":
    commandline_options()
