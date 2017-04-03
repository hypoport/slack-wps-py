from unittest import TestCase
from wpsParser import WpsParser
import logging


class TestWpsParser(TestCase):
    def setUp(self):
        self.wps = WpsParser()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def test_parse(self):
        self.assertEqual(self.wps.parse("foo"), "bar")
