import unittest
from my_test_api import TestAPI


class TestListIssues(TestAPI):

    def test_filter(self):
        params = {
            'filter': 'bla bla bla'
        }
        response = self.get(self.build_url('/issue/', params))

        self.assertEquals(response.status_code, 200)
        # self.assertEquals(response.parsed['issue']['@id'], 'API-1')
        # print response.parsed

    def test_filter_unexists(self):
        params = {
            'filter': 'SDFLWl3erkl23rl238sl32ir'
        }
        response = self.get(self.build_url('/issue/', params))

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.parsed['issueCompacts'], None)

    # def test_with(self):
    #     response = self.get('/issue/' + 'AAA-ZZZ')
    #     self.assertEquals(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()