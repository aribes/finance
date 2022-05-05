import logging
import yaml
import os

class config:

    def __init__(self) -> None:
        self.logger = None
        self.engine = None
        self.engine_1_4 = None
        self.db_manager = None
        self.date_format = '%Y-%m-%d'
        self.user_categories = {}
        self.user_bank_files = {}
        self.init_logging()

    def init_logging(self):
        self.logger = logging.getLogger("App")
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        self.logger.addHandler(console_handler)

    def load_config_files(self):

        categories_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'categories.yaml')
        bank_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'bank_files.yaml')
        with open(categories_file) as f:
            self.user_categories = yaml.load(f, Loader=yaml.FullLoader)
        with open(bank_file) as f:
            self.user_bank_files = yaml.load(f, Loader=yaml.FullLoader)
        pass

    def get_database_url(self):

        # TODO - Parameters to choose one that is not the default
        # TODO - Check the file is correct
        # Using Sqlite by default

        # Find Default
        bank_name = self.user_bank_files['databases']['Default']
        db_filename = self.user_bank_files['databases'][bank_name]
        database_url = 'sqlite:///' + db_filename
        return database_url

    def is_category_defined(self, category):
        categories = self.user_categories['categories']
        values = sum(list(categories.values()), []) + list(categories.keys())
        return category in values


c = config()
