import logging


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


c = config()
