import re
import os
import shutil

""" For a specified XML file, when user supplies a dict of key-value pairs of XML-attributes and XML-values,
    the script will replace the values for the attributes with the values supplied in the dict.

    Usage: Edit the script; in the main section, replace the following variable assignments:
        1. specify the path of the XML file (`file_path_source`)
        2. specify a dict of XML attribute-value pairs (`attribute_keys_to_update`)

    Returns: Updates the XML file. Creates a backup of original, named FILENAME_ORIG.xml
"""


def get_abs_file_path(relative_file_location):
    """ Returns absolute file path of given file

    :param relative_file_location:
    :return:
    """

    # absolute directory of this script file:
    script_directory = os.path.dirname(__file__)

    # return absolute path of file:
    return os.path.join(script_directory, relative_file_location)


def suffixed_file_name(file_path, suffix_string):
    """ Returns file path with appended string (preserving file type)

    :param file_path: (string) either relative or absolute path of file
    :param suffix_string: (string) string to append to the original file name

    :return: (string) suffixed file path

    example:
        append_path("foo.html.bar.html", "_BAZ")
        >>> "foo.html.bar.html_BAZ.html"
    """

    # reverse split, with max of 1 split:
    string_parts = file_path.rsplit('.', 1)

    return string_parts[0] + suffix_string + '.' + string_parts[1]


def backup_XML(file_path):
    """ Makes backup of XML file as FILENAME_ORIG.xml

    :param file_path: (string) absolute path of file

    :return: (None)
    """

    # rename backup file with suffix, '_ORIG':
    backup_file_path = suffixed_file_name(file_path, '_ORIG')

    # make backup of file:
    shutil.copy2(file_path, backup_file_path)


def update_attributes(file_path, keys_values_to_update):
    """ open and read file

    :param file_path: (string) specifies file path of an XML file
    :param keys_values_to_update: (dict) key-value pairs, where key corresponds to XML's `name` attribute and value
           corresponds to XML's `value` attribute.

    :return: (None)
    """

    # create regex for capturing value for 'name' attribute inside an XML tag
    # i.e. `<setParameter name="IIS Web Application Name" />` will create capture group for
    # "IIS Web Application Name" (minus quotes):
    # (n.b. regex permissive to spaces):
    name_attribute_regex = re.compile(r'''
    <\ *                   # starts with `<`
    .*                     # anything
    name\ *=\ *"           # `name="`
    (.[^"]*)"              # capture group (anything) followed by quote
    .*                     # anything
    >                      # ends with `>`
    ''', re.VERBOSE)

    # since we already match the entire tag in the above regex (`name_attribute_regex`), and since we want to only
    # capture the regex of the value attribute
    value_attribute_regex = re.compile(r'''
    value\ *=\ *"          # `value="`
    (.[^"]*)"              # capture group (anything) followed by quote
    ''', re.VERBOSE)

    # read file and make updates in-memory:
    output = ''
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # find the regex's capture group:
                name_regex_match = re.search(name_attribute_regex, line)
                name_attribute_in_file = name_regex_match.groups(0)[0]

                # if the attribute is one that needs to be updated (as specified in user-passed dict),
                # then replace the tag's `value` attribute:
                if name_attribute_in_file in keys_values_to_update:
                    line = re.sub(value_attribute_regex,
                                  'value="%s"' % (keys_values_to_update[name_attribute_in_file]),
                                  line)

                    print('Attribute "%s" changed to "%s"'
                          % (name_attribute_in_file, keys_values_to_update[name_attribute_in_file]))

            # if a line (XML tag) doesn't have the `name` attribute, ignore line:
            except AttributeError as e:
                pass

            output += line

    # write-out changes to file:
    with open(file_path, 'w+') as file:
        file.write(output)
        print('\nWrote to', file_path)


def update_XML(file_path, keys_values_to_update):
    """ Main function for updating XML attributes; calls helper methods.

    :param file_path: (string) path to source file
    :param keys_values_to_update: (dict) key-value pairs corresponding to XML attributes and their new values

    :return:
    """

    # get absolute path of XML file (from given its relative path):
    file_path = get_abs_file_path(file_path)

    # save a backup of XML file:
    backup_XML(file_path)

    # update attributes of XML and save file:
    update_attributes(file_path, keys_values_to_update)

####################################
#               Main
####################################

if __name__ == '__main__':
    # TODO: set file path:
    file_path_source = 'tests/input.SetParameters.xml'

    # TODO: replace key-value pairs with parameters to replace:
    attribute_keys_to_update = {
        'EnvironmentBannerText': 'MEOW MEOW MEOW',
        'ServerURL': 'OINK A DOINK'
    }

    update_XML(file_path_source, attribute_keys_to_update)
