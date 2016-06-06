import time
import unittest
from my_test_api import TestAPI


class TestDeleteIssue(TestAPI):

    def test_delete_issue(self):

        params = {
            'project': 'API',
            'summary': 'for deleting',
            'description': 'this issue must remove',
        }
        issue_id = self.create_item('/issue/', params)
        print('Created issue ', issue_id)

        url = '/issue/'+issue_id
        response = self.delete(url)
        self.assertEqual(response.status_code, 200)

        time.sleep(1)
        response = self.get(url)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()