import re


# TODO: should do a backup of web.config before making any changes
def backup_webconfig():
    pass


def update_parameters(file_name, keys_values_to_update):
    """ open and read file

    :param file_name: (string) specifies file path of *.SetParameters.xml
    :param keys_values_to_update: (dict) key-value pairs, where key corresponds to XML's `name` property and value
            corresponds to XML's `value` property.
    :return:
    """
    # create regex for capturing value for 'name' property inside <setParameter />
    # i.e. `<setParameter name="IIS Web Application Name" />` will create capture group for
    # "IIS Web Application Name" (minus quotes):
    name_property_regex = re.compile(r'''
    <\ *setParameter      # starts with `<setParameter` (n.b. permits spaces)
    .*                     # anything
    name\ *=\ *"           # `name="` (n.b. permits spaces)
    (.[^"]*)"              # capture group followed by quote
    .*                     # anything
    >\W*$                  # ends with `>` and space char
    ''', re.VERBOSE)


    with open(file_name, 'r+') as file:
        for line_in_text in file:
            try:
                match = re.search(name_property_regex,
                                  line_in_text)
                print(match.groups(0)[0])
            except AttributeError as e:
                pass

####################################
#               Main
####################################
if __name__ == '__main__':
    parameter_keys_to_update = {
        'EnvironmentBannerText': 'MEOW MIX',
        'ServerURL': 'OINKY DOINKY'
    }

    update_parameters('Co-constructSite.SetParameters.xml', parameter_keys_to_update)
