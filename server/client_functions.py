#!/usr/bin/env python3

from datetime import datetime
import os
import sys
import re
import argparse
import pandas
import logging

from finance_lib import *

def init_arg_parser():
  parser = argparse.ArgumentParser()
  # Basic arguments
  parser.add_argument("--db", help="Select db file")
  parser.add_argument("--date", help="Select a specific filter date")

  # CSV arguments
  parser.add_argument("--add_csv", help="Add CSV file to the database")
  parser.add_argument("--csv_version", default="", help="Set CSV file version")

  # Regexes arguments
  parser.add_argument("--regex_category", help="New Regex Category")
  parser.add_argument("--regex_definition", help="New Regex Definition")
  parser.add_argument("--test_regex", help="Test New Regex", action="store_true")
  parser.add_argument("--apply_regex", help="Apply New Regex", action="store_true")
  parser.add_argument("--apply_regexes", help="ReApply New Regex", action="store_true")
  parser.add_argument("--apply_custom", help="Apply Custom", action="store_true")

  # Statistics
  parser.add_argument("--stats", help="Compute and Show statistics", action="store_true")
  parser.add_argument("--display_categories", help="Display categories", action="store_true")
  parser.add_argument("--display_category", help="Display category")
  parser.add_argument("--list_categories", help="List Categories", action="store_true")

  return parser

def update_data(args):
  if args.add_csv:
    logging.info('Adding CSV file to the database: {}'.format(args.add_csv))
    pd = utils_csv.import_csv_file(args.add_csv, args.csv_version)
    utils_csv.add_pd_to_db(pd)
    utils_regex.apply_regexes_to_data()
    utils_regex.apply_custom_regex()

  if args.test_regex and args.regex_category and args.regex_definition:
    logging.info("Testing regex cat: {} - def: {}".format(args.regex_category, args.regex_definition))
    utils_regex.run_regex(args.regex_definition, args.regex_category, apply=False)

  if args.apply_regex and args.regex_category and args.regex_definition:
    logging.info("Applying and adding regex cat: {} - def: {}".format(args.regex_category, args.regex_definition))
    utils_regex.run_regex(args.regex_definition, args.regex_category, apply=True)

  if args.apply_regexes:
    utils_regex.apply_regexes_to_data()

  if args.apply_custom:
    utils_regex.apply_custom_regex()

def display_data(args):
  # TODO - Filter data
  if args.stats:
    utils_term_ouput.show_statistics()

  if args.list_categories:
    utils_term_ouput.show_categories()

  if args.display_categories:
    utils_term_ouput.show_categories_content()

  if args.display_category:
    utils_term_ouput.show_category_content(args.display_category)