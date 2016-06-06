import time
import unittest
from my_test_api import TestAPI


class TestUpdateIssue(TestAPI):

    def test_update_issue(self):

        params = {
            'project': 'API',
            'summary': 'bla bla bla',
            'description': 'A description',
        }
        issue_id = self.create_item('/issue/', params)
        print('Created issue ', issue_id)

        data = {
            'summary': 'updated awesome text',
            'description': 'updated weird description'
        }
        url = '/issue/'+issue_id
        response = self.post(url, data)
        self.assertEqual(response.status_code, 200)

        time.sleep(1)
        response = self.get(url)

        summary = ''
        descr = ''
        for field in response.parsed['issue']['field']:
            if field['@name'] == 'summary':
                summary = field['value']
            if field['@name'] == 'description':
                descr = field['value']

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.parsed['issue']['@id'], issue_id)
        self.assertEqual(summary, 'updated awesome text')
        self.assertEqual(descr, 'updated weird description')

        # and then we should delete tested issue
        self.delete(url)

if __name__ == '__main__':
    unittest.main()