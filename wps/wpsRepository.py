import logging
from wps.commandType import CommandType


class WpsRepository:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def add(self, command: dict):
        self.logger.info('adding %s..', command)

    def get(self, command: dict):
        self.logger.info('getting %s..', command)
