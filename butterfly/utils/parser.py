import argparse
import ConfigParser
import os

from butterfly.utils.utils import get_dir_of


config_dict = dict()


def parser(config):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config)

    for section in config_parser.sections():
        config_dict[section] = dict()
        for key, val in config_parser.items(section):
            config_dict[section][key] = val
    return config_dict

BUTTERFLY_CONF = "etc/butterfly.conf"

arg_parser = argparse.ArgumentParser(description="Process the user input")
arg_parser.add_argument('--config', type=str, help="Configuration file")
arg_parser.add_argument('--action', type=str, help="Performs the action")
args = arg_parser.parse_args()

ACTION = args.action
config = args.config
config_path = os.path.join(get_dir_of(__file__), BUTTERFLY_CONF)
if config:
    config_path = config
config = parser(config_path)
