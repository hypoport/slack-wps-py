import logging
import dateparser
from datetime import datetime, time
from commandType import CommandType


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text: str) -> dict:
        self.logger.info('start parsing %s..', text)

        status_or_users = None
        if 'from' in text:
            textparts = text.split(' from ')
            status_or_users = textparts[0]
            dates = textparts[1].split(' to ')
            from_date = dateparser.parse(dates[0])
            to_date = dateparser.parse(dates[1])
        elif 'on' in text:
            textparts = text.split(' on ')
            status_or_users = textparts[0]
            on_date = dateparser.parse(textparts[1])
            from_date = datetime.combine(on_date, time.min)
            to_date = datetime.combine(on_date, time.max)
        else:
            status_or_users = text
            from_date = dateparser.parse('today')
            to_date = dateparser.parse('today, 23:59:59.999999')

        command = {
            'from': from_date,
            'to': to_date
        }
        self.parse_status_or_users(status_or_users, command)

        return command

    def parse_status_or_users(self, status_or_users: str, command: dict):
        if status_or_users.startswith('@'):
            command['commandType'] = CommandType.GET
            command['users'] = status_or_users.split()
        else:
            command['commandType'] = CommandType.SET
            command['status'] = status_or_users.strip()
