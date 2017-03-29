import argparse
import os

import parser as conf_parser
from butterfly.db import actions

DB_INIT = "db_init"
DB_DROP = "db_drop"
DB_UPGRADE = "db_upgrade"
RUN = "run"

arg_parser = argparse.ArgumentParser(description="Process the user input")
arg_parser.add_argument('--config', type=str, help="Configuration file")
arg_parser.add_argument('--action', type=str, help="Performs the action")
args = arg_parser.parse_args()

ACTION = args.action
config = args.config
config_path = os.path.dirname(os.path.abspath(__file__)) + "/etc/butterfly.conf"
if config:
    config_path = config
config = conf_parser.parser(config_path)


def main():
    if ACTION == DB_INIT:
        actions.register_tables(config)
    elif ACTION == DB_DROP:
        actions.unregister_tables(config)
    elif ACTION == RUN:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
