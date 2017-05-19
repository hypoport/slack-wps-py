from unittest import TestCase
from wpsParser import WpsParser
import logging
from commandType import CommandType


class TestWpsParser(TestCase):
    def setUp(self):
        self.wps = WpsParser()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def test_parse(self):
        self.assertEqual(self.wps.parse("foo", None), "bar")

    def test_parse_set_status_from_to(self):
        # dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
        # dict['Age'] = 8;  # update existing entry
        # dict['School'] = "DPS School";  # Add new entry
        #
        # print "dict['Name']: ", dict['Name']

        expected_command = {
            'commandType': CommandType.SET,
            'status': 'sick',
            'from': 'foo',
            'to': 'bar',
            'user': 'me'
        }
        command = self.wps.parse("sick from a date to another date", 'me')
        self.assertEqual(command, expected_command)

    def test_parse_get_status_from_to(self):
        expected_command = {
            'commandType': CommandType.GET,
            'users': ['me', 'him'],
            'from': 'foo',
            'to': 'bar'
        }
        command = self.wps.parse("@group", 'me')
        self.assertEqual(command, expected_command)
