import xmltodict
import json
import requests


class Api(object):
    """
        Provides API calls by GET, POST, PUT, DELETE methods
    """

    name = None
    settings = None
    credentials = None
    cookies = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_settings(self, settings):
        self.settings = settings
        if 'should_parse_response' not in self.settings:
            self.settings['should_parse_response'] = False

    def has_settings(self):
        return self.settings is not None

    def check_settings(self):
        assert self.settings is not None, 'Should set settings before login'
        assert 'credentials' in self.settings, 'Should set credentials in the settings'
        assert 'login' in self.settings['credentials'], 'Should set login in the settings'
        assert 'password' in self.settings['credentials'], 'Should set password in the settings'
        assert 'base_url' in self.settings, 'Should set base_url in the settings'
        assert 'auth_endpoint' in self.settings, 'Should set auth_endpoint in the settings'
        assert 'auth_way' in self.settings, 'Should set auth_way in the settings'

    def base_url(self):
        if 'base_url' in self.settings:
            return self.settings['base_url']
        return None

    def auth(self):
        if self.is_logged():
            return

        params = {
            'login': self.settings['credentials']['login'],
            'password': self.settings['credentials']['password']
        }

        url = self.base_url() + self.settings['auth_endpoint']
        response = requests.post(url, data=params)

        if len(response.cookies):
            self.cookies = response.cookies
        else:
            self.credentials = (self.settings['credentials']['login'], self.settings['credentials']['password'])

    def is_logged(self):
        return (self.cookies is not None and len(self.cookies) > 0) or \
               (self.credentials is not None and len(self.credentials) > 0)

    def get(self, endpoint):
        """
        Improves GET request to base API url with endpoint
        Args:
            endpoint (string): the target API url without base url
        """
        url = self.base_url() + endpoint
        authority = self.__get_credentials()
        response = requests.get(url, **authority)
        return self.__parseResponse(response)

    def post(self, endpoint, params=None):
        if params is None:
            params = []
        url = self.base_url() + endpoint
        authority = self.__get_credentials()
        response = requests.post(url, data=params, **authority)
        return self.__parseResponse(response)

    def put(self, endpoint, params=None):
        if params is None:
            params = []
        url = self.base_url() + endpoint
        authority = self.__get_credentials()
        response = requests.put(url, data=params, **authority)
        return self.__parseResponse(response)

    def delete(self, endpoint):
        url = self.base_url() + endpoint
        authority = self.__get_credentials()
        response = requests.delete(url, **authority)
        return self.__parseResponse(response)

    def create_item(self, endpoint, params=None):
        if params is None:
            params = {}
        response = self.put(endpoint, params)
        if response.status_code == 201 and len(response.headers['Location']):
            return response.headers['Location'].split('/')[-1]
        else:
            return None

    def __get_credentials(self):
        if self.credentials is not None:
            params = {'auth': self.credentials}
        elif self.cookies is not None:
            params = {'cookies': self.cookies}
        else:
            params = {}
        return params

    def __parseResponse(self, response):
        if self.settings['should_parse_response'] == False:
            return response
        if hasattr(response, 'text') and len(response.text):
            if self.settings['should_parse_response'] == 'xml':
                response.parsed = xmltodict.parse(response.text)
            if self.settings['should_parse_response'] == 'json':
                response.parsed = json.load(response.text)
        return response