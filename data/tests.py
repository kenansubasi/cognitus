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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 10)

    def test_data_create(self):
        url = "/api/v1/data/"
        data = {
            "text": "evet",
            "label": "Confirmation_Yes"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content.get("text"), "evet")
        self.assertEqual(content.get("label"), "Confirmation_Yes")

        data_id =  content.get("id")
        retrieve_url = f"/api/v1/data/{data_id}/"
        response = self.client.get(retrieve_url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), data_id)
        self.assertEqual(content.get("text"), "evet")
        self.assertEqual(content.get("label"), "Confirmation_Yes")
        self.assertEqual(content.get("creator", {}).get("username"), self.USER_USERNAME)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_data_retrieve(self):
        url = f"/api/v1/data/{self.DATA_ID}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.DATA_ID)
        self.assertEqual(content.get("text"), self.DATA_TEXT)
        self.assertEqual(content.get("label"), self.DATA_LABEL)
        self.assertEqual(content.get("creator", {}).get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("created_at"), "2020-03-29T01:00:00Z")
        self.assertEqual(content.get("updated_at"), "2020-03-29T01:00:00Z")

    def test_data_update(self):
        url = f"/api/v1/data/{self.DATA_ID}/"
        data = {
            "text": "evet",
            "label": "Confirmation_Yes"
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.put(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.DATA_ID)
        self.assertEqual(content.get("text"), "evet")
        self.assertEqual(content.get("label"), "Confirmation_Yes")

        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.DATA_ID)
        self.assertEqual(content.get("text"), "evet")
        self.assertEqual(content.get("label"), "Confirmation_Yes")
        self.assertEqual(content.get("creator", {}).get("username"), self.USER_USERNAME)

        different_user_data_url = f"/api/v1/data/4/"
        response = self.client.put(different_user_data_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_data_destroy(self):
        url = f"/api/v1/data/{self.DATA_ID}/"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        different_user_data_url = f"/api/v1/data/4/"
        response = self.client.delete(different_user_data_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
