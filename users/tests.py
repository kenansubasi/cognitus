import json

from rest_framework import status

from cognitus.tests import CognitusApiV1TestCase


class UserApiTestCase(CognitusApiV1TestCase):
    fixtures = ("test_user",)

    def test_user_login(self):
        url = f"{self.API_URL}/login/"
        data = {
            "username": self.USER_USERNAME,
            "password": self.USER_PASSWORD
        }

        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.USER_ID)
        self.assertEqual(content.get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("first_name"), "Admin")
        self.assertEqual(content.get("last_name"), "Cognitus")
        self.assertContains(response, "auth_token")

    def test_user_logout(self):
        url = f"{self.API_URL}/logout/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        url = f"{self.API_URL}/users/{self.USER_USERNAME}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.USER_ID)
        self.assertEqual(content.get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("first_name"), "Admin")
        self.assertEqual(content.get("last_name"), "Cognitus")
