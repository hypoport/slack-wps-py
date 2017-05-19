import logging
import dateparser
from datetime import datetime, time
from commandType import CommandType


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text, user):
        self.logger.info('start parsing..')
        self.logger.info(text)
        self.logger.info(dateparser.parse('heute'))
        my_date = dateparser.parse('morgen')
        self.logger.info(my_date)

        min_pub_date_time = datetime.combine(my_date, time.min)
        self.logger.info(min_pub_date_time)
        max_pub_date_time = datetime.combine(my_date, time.max)
        self.logger.info(max_pub_date_time)

        command = {'commandType': CommandType.SET, 'user': user}
        return command
