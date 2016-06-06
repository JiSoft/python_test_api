import unittest
from my_test_api import TestAPI


class TestCreateIssue(TestAPI):

    def test_create_issue(self):

        params = {
            'project': 'API',
            'summary': 'test issue by robots',
            'description': 'You are mine ! ',
        }

        response = self.put('/issue/', params)
        issue_id = response.headers['Location'].split('/')[-1]
        print('Created item ID is ', issue_id)
        self.assertEquals(response.status_code, 201)

        response = self.get('/issue/' + issue_id)
        self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()