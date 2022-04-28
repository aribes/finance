#!/usr/bin/env python3

from client_functions import init_arg_parser, run
import finance_lib as fl


args = init_arg_parser().parse_args()
cfg = fl.utils_cfg.cfg


# Parser Date
# cfg.load_date(args.date)
# if cfg.wanted_year:
#   logging.info("Selected date Y:{} M:{} D:{}".format(cfg.wanted_year, cfg.wanted_month, cfg.wanted_day))

# Load / Init load DB
db_filename = "bank_australia.db"
if args.db:
  db_filename = args.db

# Using Sqlite by default
database_url = 'sqlite:///' + db_filename

fl.config.c.logger.info("Starting ORM version")
fl.config.c.db_manager = fl.db_manager.DatabaseManager(database_url)

# TODO - To put in args
# TODO - Use agnostic path system
configuration_file = '../config/categories.yaml'
fl.config.c.load_config_file(configuration_file)

run(args)
