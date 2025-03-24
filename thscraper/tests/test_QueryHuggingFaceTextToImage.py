import unittest
from unittest import mock, skip

from thscraper.queries.QueryHuggingFace import QueryHFTTI

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    if kwargs['json']['inputs'] == 'success':
        return MockResponse('okay', 200)
    elif kwargs['json']['inputs'] == 'error':
        return MockResponse('error', 404)

    return MockResponse(None, 404)

@skip("LLM breaks mocks")
class Test(unittest.TestCase):
    @mock.patch('thscraper.queries.QueryHuggingFace.requests.post', side_effect=mocked_requests_post)
    def test_parse_hftti_with_success(self, mock_get):
        qw = QueryHFTTI()
        result = qw.query('success')
        self.assertEqual(result, 'okay')

    @mock.patch('thscraper.queries.QueryHuggingFace.requests.post', side_effect=mocked_requests_post)
    def test_parse_hftti_with_failure(self, mock_get):
        qw = QueryHFTTI()
        result = qw.query('error')
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()
