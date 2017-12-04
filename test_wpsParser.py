from unittest import TestCase
from wpsParser import WpsParser
import logging
from commandType import CommandType
from libfaketime import fake_time, reexec_if_needed
from datetime import datetime


class TestWpsParser(TestCase):
    reexec_if_needed()

    def setUp(self):
        self.wps = WpsParser()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @fake_time('1970-12-14 13:05:15')
    def test_parse_set_status_from_to(self):
        expected_command = {
            'commandType': CommandType.SET,
            'status': 'sick',
            'from': datetime(1970, 12, 14+1, 13+1, 5, 15),  # check timezones - why 13+1 not 13?
            'to': datetime(1970, 12, 14+3, 13+1, 5, 15)     # check timezones - why 13+1 not 13?
        }
        command = self.wps.parse("sick from tomorrow to in 3 days")
        self.assertEqual(expected_command, command)

    @fake_time('1970-12-10 13:05:15')
    def test_parse_set_status_on(self):
        expected_command = {
            'commandType': CommandType.SET,
            'status': 'sick',
            'from': datetime(1970, 12, 10+1, 0, 0, 0),
            'to': datetime(1970, 12, 10+1, 23, 59, 59, 999999)
        }
        command = self.wps.parse("sick on tomorrow")
        self.assertEqual(expected_command, command)

    @fake_time('1970-12-21 16:35:10')
    def test_parse_set_status(self):
        expected_command = {
            'commandType': CommandType.SET,
            'status': 'sick',
            'from': datetime(1970, 12, 21, 16+1, 35, 10),  # check timezones - why is dateparser.parse('today') 17h and nor 16h?
            'to': datetime(1970, 12, 21, 23, 59, 59, 999999)
        }
        command = self.wps.parse("sick")
        self.assertEqual(expected_command, command)

    def test_parse_get_status(self):
        expected_command = {
            'commandType': CommandType.GET,
            'users': ['@john']
        }
        command = self.wps.parse("@john")
        self.assertEqual(expected_command, command)
