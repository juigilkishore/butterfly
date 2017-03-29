import ConfigParser

config_dict = dict()


def parser(config):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config)

    for section in config_parser.sections():
        config_dict[section] = dict()
        for key, val in config_parser.items(section):
            config_dict[section][key] = val
    return config_dict
