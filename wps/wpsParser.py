import logging
import dateparser
from datetime import datetime, time
from wps.commandType import CommandType


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text: str) -> dict:
        self.logger.info('start parsing %s..', text)

        settingsWithTimeMin = {'RELATIVE_BASE': datetime.combine(datetime.today().date(), time.min)}
        settingsWithTimeMax = {'RELATIVE_BASE': datetime.combine(datetime.today().date(), time.max)}
        status_or_users = None
        if 'from' in text:
            textparts = text.split(' from ')
            status_or_users = textparts[0]
            dates = textparts[1].split(' to ')
            from_date = dateparser.parse(dates[0], settings=settingsWithTimeMin)
            to_date = dateparser.parse(dates[1], settings=settingsWithTimeMax)
        elif 'on' in text:
            textparts = text.split(' on ')
            status_or_users = textparts[0]
            from_date = dateparser.parse(textparts[1], settings=settingsWithTimeMin)
            to_date = datetime.combine(from_date.date(), time.max)
        else:
            status_or_users = text
            from_date = datetime.today()
            to_date = datetime.combine(from_date.date(), time.max)

        command = {
            'from': from_date,
            'to': to_date
        }
        self.parse_status_or_users(status_or_users, command)

        # entweder ein command vom typ GET mit users oder vom typ SET mit status
        return command

    def parse_status_or_users(self, status_or_users: str, command: dict):
        if status_or_users.startswith('@'):
            command['commandType'] = CommandType.GET
            command['users'] = status_or_users.replace('@', '').split()
        else:
            command['commandType'] = CommandType.SET
            command['status'] = status_or_users.strip()
