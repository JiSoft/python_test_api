import os
from base.base_test_api import BaseTestAPI


class TestAPI(BaseTestAPI):

    def setUp(self):
        self.set_name('YouTrack')
        self.load_settings(os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/settings.yaml')
        self.auth()
