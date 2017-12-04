import logging
import dateparser
from datetime import datetime, time
from commandType import CommandType


class WpsParser:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def parse(self, text: str) -> dict:
        self.logger.info('start parsing %s..', text)

        if text.startswith('@'):
            return self.parse_get(text)
        else:
            return self.parse_set(text)

    def parse_get(self, text: str) -> dict:
        command = {
            'commandType': CommandType.GET
        }
        return command

    def parse_set(self, text: str) -> dict:
        if 'from' in text:
            textparts = text.split(' from ')
            status = textparts[0].strip()
            dates = textparts[1].split(' to ')
            from_date = dateparser.parse(dates[0])
            to_date = dateparser.parse(dates[1])
        elif 'on' in text:
            textparts = text.split(' on ')
            status = textparts[0].strip()
            on_date = dateparser.parse(textparts[1])
            from_date = datetime.combine(on_date, time.min)
            to_date = datetime.combine(on_date, time.max)
        else:
            status = text.strip()
            from_date = dateparser.parse('today')
            to_date = dateparser.parse('today, 23:59:59.999999')

        command = {
            'commandType': CommandType.SET,
            'status': status,
            'from': from_date,
            'to': to_date
        }
        return command


