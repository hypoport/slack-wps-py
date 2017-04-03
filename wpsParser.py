import logging


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text):
        self.logger.info('start parsing..')
        self.logger.info(text)
        return "bar"
