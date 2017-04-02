import argparse
import os

import parser as conf_parser
from butterfly.db import actions as db_actions
from butterfly.utils import get_dir_of

DB_INIT = "db_init"
DB_ADD = "db_add"
DB_DROP = "db_drop"
DB_UPGRADE = "db_upgrade"
RUN = "run"

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
config = conf_parser.parser(config_path)


def main():
    if ACTION == DB_INIT:
        db_actions.register_tables(config)
    elif ACTION == DB_DROP:
        db_actions.unregister_tables(config)
    elif ACTION == DB_ADD:
        db_actions.update_tables(config)
    elif ACTION == RUN:
        pass

if __name__ == "__main__":
    main()
