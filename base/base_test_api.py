import api
import unittest
import urllib
from yaml import load


class BaseTestAPI(unittest.TestCase, api.Api):

    def load_settings(self, file_path):
        if self.has_settings():
            return

        with open(file_path) as f:
            self.set_settings(load(f.read()))
        self.check_settings()

    def build_url(self, url, params=None):
        if params is None:
            params = {}
        if len(params):
            return url + '?' + urllib.urlencode(params)
        return url
