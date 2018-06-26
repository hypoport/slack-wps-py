import logging
import re
import dateparser
from datetime import datetime, time
from wps.commandType import CommandType


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text: str) -> dict:
        self.logger.info('start parsing %s..', text)

        strippedText = text.strip()
        if strippedText.startswith("clear"):
            return {'commandType': CommandType.CLEAR}

        if strippedText.startswith('<!subteam^'):
            command = {
                'commandType': CommandType.GET_GROUP,
                'group': re.search('<!subteam\^(.*)\|', strippedText).group(1)
            }
            return command

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
            'from_date': from_date,
            'to_date': to_date
        }
        self.parse_status_or_users(status_or_users, command)
        return command

    def parse_status_or_users(self, status_or_users: str, command: dict):
        if status_or_users.startswith('@'):
            command['commandType'] = CommandType.GET
            command['users'] = status_or_users.replace('@', '').split()
        else:
            command['commandType'] = CommandType.SET
            status = self.map_status(status_or_users.strip())
            command['status'] = status

    def map_status(self, status):
        if status in ['krank', 'sick']:
            return 'sick'
        elif status in ['vacation', 'vacay', 'vaca','vac','urlaub']:
            return 'vacation'
        elif status in ['offline','off','afk']:
            return 'offline'
        elif status in ['homeoffice', 'ho', 'hangover']:
            return 'homeoffice'
        elif status in ['remote','rmt']:
            return 'remote'
        elif status in ['workoffice','wo']:
            return 'workoffice'
        else:
            self.logger.info('Illegal status: ' + status )
            raise ValueError('Illegal status: '+ status)

