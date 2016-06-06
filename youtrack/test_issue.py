import unittest
from my_test_api import TestAPI


class TestGetIssue(TestAPI):

    def test_get_issue(self):
        response = self.get('/issue/' + 'API-1')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.parsed['issue']['@id'], 'API-1')

    def test_get_absent_issue(self):
        response = self.get('/issue/' + 'AAA-ZZZ-DDD')
        self.assertEquals(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()