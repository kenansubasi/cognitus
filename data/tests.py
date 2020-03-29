import json

from rest_framework import status

from cognitus.tests import CognitusApiTestCase


class DataApiTestCase(CognitusApiTestCase):
    fixtures = ("test_user", "test_data")

    def test_data_list(self):
        url = "/api/v1/data/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 10)
