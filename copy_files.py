import os
import shutil

""" Copies files from source to destination.
    Options:g

"""

ALLOWED_FILES = frozenset({"jpg", "jpeg", "gif", "ico", "png"})


def copy_files(source, target, filter_option=""):
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
            if filter_option == "largest-per-folder":
                largest_file = max(filtered_files_full_path, key=lambda file_: os.stat(file_).st_size)
                files_to_copy.append(largest_file)

            # For each dir_, add only the smallest image for copying:
            elif filter_option == "smallest-per-folder":
                largest_file = min(filtered_files_full_path, key=lambda file_: os.stat(file_).st_size)
                files_to_copy.append(largest_file)

            # If no custom filter present, add all images for copying:
            else:
                files_to_copy.extend(filtered_files_full_path)
        except ValueError as e:
            pass

    # -----------------------------------------------
    # Copy files to target:

    # Copy files:
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
    copy_files("source", "target", "largest-per-folder")
