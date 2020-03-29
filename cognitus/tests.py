from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase


class CognitusTestCase(TestCase):
    USER_ID = 1
    USER_USERNAME = "admin"
    USER_PASSWORD = "secret"  # common password for each user.
    DATA_ID = 1
    DATA_TEXT = "olmaz"
    DATA_LABEL = "Confirmation_No"

    @classmethod
    def setUpClass(cls):
        """
        Support YAML format in the fixtures.
        """
        if cls.fixtures:
            new_fixtures = []
            for fixture_name in cls.fixtures:
                new_fixtures.append(f"{settings.FIXTURE_YAML_DIR}/{fixture_name}.yaml")
            cls.fixtures = new_fixtures

        super(CognitusTestCase, cls).setUpClass()


class CognitusApiV1TestCase(CognitusTestCase):
    API_URL = "/api/v1"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username=self.USER_USERNAME)
        self.token, created = Token.objects.get_or_create(user=self.user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
