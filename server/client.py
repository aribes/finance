#!/usr/bin/env python3

from client_functions import *
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

db_mgt = fl.db.db_manager(db_filename)
cfg.db_connection = db_mgt.engine.connect()
cfg.data_table = db_mgt.data_table
cfg.regexes_table = db_mgt.regexes_table
cfg.session = db_mgt.session

update_data(args)
display_data(args)