from butterfly.utils import parser
from butterfly.api import server
from butterfly.db import actions as db_actions

DB_INIT = "db_init"         # Initialization
DB_ADD = "db_add"           # Add Database
DB_DROP = "db_drop"         # Drop Database
DB_UPGRADE = "db_upgrade"   # Upgrade Database
RUN = "run"

ACTION = parser.ACTION
config = parser.config


def main():
    if ACTION == DB_INIT:
        db_actions.register_tables(config)
    elif ACTION == DB_DROP:
        db_actions.unregister_tables(config)
    elif ACTION == DB_ADD:
        db_actions.update_tables(config)
    elif ACTION == RUN:
        server.run(config)

if __name__ == "__main__":
    main()
