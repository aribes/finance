#!/usr/bin/env python3

import argparse
import logging

from finance_lib import *
from finance_lib import config
from finance_lib import csv
from finance_lib import categoriser
from finance_lib import utils_term_ouput
from finance_lib import db_tables

from sqlalchemy.orm import Session


def init_arg_parser():

  parser = argparse.ArgumentParser()
  
  # Basic arguments
  parser.add_argument("--db", help="Select db file")
  parser.add_argument("--date", help="Select a specific filter date")

  # CSV arguments
  parser.add_argument("--add_csv", help="Add CSV file to the database")
  parser.add_argument("--csv_version", default="", help="Set CSV file version")

  # Categoriser arguments
  parser.add_argument("--categoriser_regex", help="New Regex Category")
  parser.add_argument("--categoriser_category", help="New Regex Definition")
  parser.add_argument("--id", help="Categoriser Id", type=int)
  parser.add_argument("--test", help="Test New Regex", action="store_true")
  parser.add_argument("--add", help="Add and Apply New Regex", action="store_true")
  parser.add_argument("--update", help="Update Categoriser", action="store_true")
  parser.add_argument("--delete", help="Delete Categoriser", action="store_true")
  parser.add_argument("--reapply_categorisers", help="ReApply All Categorisers", action="store_true")
  parser.add_argument("--export_categorisers", help="Export Categorisers")
  parser.add_argument("--import_categorisers", help="Import Categorisers")

  # Statistics
  parser.add_argument("--stats", help="Compute and Show statistics", action="store_true")
  parser.add_argument("--list_categorisers", help="List Regexes", action="store_true")

  return parser


# TODO - We need to apply a filter from dates provided by the user
# def process_args(args):
  
#   if args.add_csv:
#     logging.info('Adding CSV file to the database: {}'.format(args.add_csv))
#     pd = utils_csv.import_csv_file(args.add_csv, args.csv_version)
#     utils_csv.add_pd_to_db(pd)

#   if args.test_regex and args.regex_category and args.regex_definition:
#     logging.info("Testing regex cat: {} - def: {}".format(args.regex_category, args.regex_definition))
#     utils_regex.run_regex(args.regex_definition, args.regex_category, apply=False)

#   if args.apply_regex and args.regex_category and args.regex_definition:
#     logging.info("Applying and adding regex cat: {} - def: {}".format(args.regex_category, args.regex_definition))
#     utils_regex.run_regex(args.regex_definition, args.regex_category, apply=True)

#   if args.apply_regexes:
#     utils_regex.apply_regexes_to_data()

#   if args.apply_custom:
#     utils_regex.apply_custom_regex()

#   if args.stats:
#     utils_term_ouput.show_statistics()

#   if args.list_categories:
#     utils_term_ouput.show_categories()

#   if args.display_categories:
#     utils_term_ouput.show_categories_content()

#   if args.display_category:
#     utils_term_ouput.show_category_content(args.display_category)


def run(args):

  if args.add_csv:
    config.c.logger.info('Adding CSV file to the database: {}'.format(args.add_csv))
    df = csv.import_bank_records_from_csv(args.add_csv)
    if df is not None:
      config.c.db_manager.add_bank_records(df)
    else:
      return

  if args.id:
    if args.delete:
      config.c.db_manager.delete_categoriser(args.id)
    elif args.update and args.categoriser_regex and args.categoriser_category:
      if not categoriser.check_categoriser(args.categoriser_regex, args.categoriser_category):
        return
      config.c.db_manager.update_categoriser(args.id, args.categoriser_regex, args.categoriser_category)

  elif args.categoriser_regex and args.categoriser_category:
    if not categoriser.check_categoriser(args.categoriser_regex, args.categoriser_category):
      return
    if args.test:
      categoriser.run_categoriser(args.categoriser_regex, args.categoriser_category, False)
    elif args.add:
      categoriser.run_categoriser(args.categoriser_regex, args.categoriser_category, True)
      config.c.db_manager.add_categoriser(args.categoriser_regex, args.categoriser_category)

  elif args.reapply_categorisers:
    with Session(config.c.engine) as session:
      for cat in session.query(db_tables.Categoriser).all():
        categoriser.run_categoriser(cat.regex, cat.category, True)
        
  elif args.export_categorisers:
    config.c.db_manager.export_categorisers(args.export_categorisers)
  elif args.import_categorisers:
    config.c.db_manager.import_categorisers(args.import_categorisers)
  elif args.list_categorisers:
    utils_term_ouput.show_categorisers()
