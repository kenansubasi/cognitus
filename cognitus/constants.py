import os

WEB_APP_DOMAIN = os.environ.get("WEB_APP_DOMAIN")
ALGORITHM_SERVICE_DOMAIN = os.environ.get("ALGORITHM_SERVICE_DOMAIN")
ALGORITHM_SERVICE_TIMEOUT = os.environ.get("ALGORIHTM_SERVICE_TIMEOUT", 60)
