import json
import os

import requests

from conf.constants import ALGORITHM_SERVICE_DOMAIN, ALGORITHM_SERVICE_TIMEOUT


class AlgorithmServiceClient(object):

    def __init__(self, base_url=None):
        self.base_url = base_url or ALGORITHM_SERVICE_DOMAIN

    def request(self, method, path, data=None, params=None, timeout=ALGORITHM_SERVICE_TIMEOUT):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.request(
            method=method,
            url=os.path.join(self.base_url, path),
            headers=headers,
            data=data,
            params=params,
            timeout=timeout
        )

        return response

    def train(self):
        return self.request("get", "train/", timeout=ALGORITHM_SERVICE_TIMEOUT)

    def prediction(self, text):
        data = json.dumps({
            "text": text
        })
        return self.request("post", "prediction/", data=data, timeout=ALGORITHM_SERVICE_TIMEOUT)
