from rest_framework.test import APIClient

from django.conf import settings
from django.test import TestCase, Client


class CognitusTestCase(TestCase):
    USER_PASSWORD = "secret"  # common password for each user.

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


class CognitusApiTestCase(CognitusTestCase):

    def setUp(self):
        self.client = APIClient()
