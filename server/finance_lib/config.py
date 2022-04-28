import logging
import yaml


class config:

    def __init__(self) -> None:
        self.logger = None
        self.engine = None
        self.db_manager = None
        self.date_format = '%Y-%m-%d'
        self.user_configs = {}
        self.init_logging()

    def init_logging(self):
        self.logger = logging.getLogger("App")
        self.logger.setLevel(logging.DEBUG)

    def load_config_file(self, config_file):
        with open(config_file) as f:
            self.user_configs = yaml.load(f, Loader=yaml.FullLoader)
            print(self.user_configs)
        pass

    def is_category_defined(self, category):
        categories = self.user_configs['categories']
        values = sum(list(categories.values()), []) + list(categories.keys())
        return category in values


c = config()
