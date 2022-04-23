import logging
import yaml


class config:

    def __init__(self) -> None:
        self.logger = None
        self.engine = None
        self.db_manager = None
        self.date_format = '%Y-%m-%d'
        self.init_logging()

    def init_logging(self):
        self.logger = logging.getLogger("App")
        self.logger.setLevel(logging.DEBUG)

    def load_config_file(self, config_file):
        with open(config_file) as f:
            user_configs = yaml.load(f, Loader=yaml.FullLoader)
            print(user_configs)
        pass


c = config()
