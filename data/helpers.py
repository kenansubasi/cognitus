import os
import requests

from django.core.exceptions import ValidationError as BaseValidationError

from cognitus.constants import ALGORITHM_SERVICE_DOMAIN, ALGORITHM_SERVICE_TIMEOUT


class AlgorithmServiceClient(object):

    def __init__(self, base_url=None):
        self.base_url = base_url or ALGORITHM_SERVICE_DOMAIN

    def request(self, method, path, data=None, params=None, timeout=ALGORITHM_SERVICE_TIMEOUT):
        response = requests.request(
            method,
            os.path.join(self.base_url, path),
            data=data,
            params=params,
            timeout=timeout
        )

        return response

    def train(self):
        return self.request("get", "train/", timeout=ALGORITHM_SERVICE_TIMEOUT)
