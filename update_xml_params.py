import re


# TODO: should do a backup of XML file before making any changes
def backup_XML():
    pass


def update_parameters(file_name, keys_values_to_update):
    """ open and read file

    :param file_name: (string) specifies file path of *.SetParameters.xml
    :param keys_values_to_update: (dict) key-value pairs, where key corresponds to XML's `name` attribute and value
            corresponds to XML's `value` attribute.
    :return:
    """
    # create regex for capturing value for 'name' attribute inside <setParameter />
    # i.e. `<setParameter name="IIS Web Application Name" />` will create capture group for
    # "IIS Web Application Name" (minus quotes):
    # (n.b. regex permissive to spaces):
    name_attribute_regex = re.compile(r'''
    <\ *setParameter       # starts with `<setParameter`
    .*                     # anything
    name\ *=\ *"           # `name="`
    (.[^"]*)"              # capture group (anything) followed by quote
    .*                     # anything
    >                      # ends with `>`
    ''', re.VERBOSE)

    # since we already match the entire tag in the above regex (`name_attribute_regex`), and since we want to only
    # to update the regex of the
    value_attribute_regex = re.compile(r'''
    value\ *=\ *"          # `value="`
    (.[^"]*)"              # capture group (anything) followed by quote
    ''', re.VERBOSE)

    # read file and make updates in-memory:
    output = ""
    with open(file_name, 'r') as file:
        for line in file:
            try:
                name_regex_match = re.search(name_attribute_regex, line)
                name_attribute_in_file = name_regex_match.groups(0)[0]

                # if the attribute is one that needs to be updated (as specified in user-passed dict),
                # then replace the tag's `value` attribute:
                if name_attribute_in_file in keys_values_to_update:
                    line = re.sub(value_attribute_regex,
                                  'value="%s"' % (keys_values_to_update[name_attribute_in_file]),
                                  line)

            # if a line (XML tag) doesn't have the `name` attribute, ignore line:
            except AttributeError as e:
                pass

            output += line

    # write-out changes to file:
    with open("updated_" + file_name, "w+") as file:
        file.write(output)

####################################
#               Main
####################################
if __name__ == '__main__':
    parameter_keys_to_update = {
        'EnvironmentBannerText': 'MEOW MEOW MEWO',
        'ServerURL': 'OINK A DOINK'
    }

    update_parameters('input.SetParameters.xml', parameter_keys_to_update)
