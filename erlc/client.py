import requests
import time
from erlc.constants import BASE_URL

import erlc.execptions as execptions


class ErlcClient:
    def __init__(self, base_url: str = None) -> None:
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def get_server(self, key: str):
        return ErlcServerClient(key, self.base_url).server.get_server()


class ErlcServerClient:
    def __init__(self, api_key: str, base_url: str = None) -> None:
        self.api_key = api_key
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Server-Key": self.api_key})
        self.rate_limit = {}
        if not self._test_key():
            raise execptions.InvalidApiKey("Invalid API key", client=self)
        from erlc.api import ServerAPI

        self.server = ServerAPI(self)

    def _test_key(self) -> bool:
        """
        Test the API key.
        """
        data = self._get("/server")
        if isinstance(data, dict) and data.get("code") == 1001:
            return False
        return True

    def _get(self, path: str, max_retries: int = 3) -> dict | requests.Response:
        """
        Get the data from the API with rate limit handling.
        """
        url = f"{self.base_url}{path}"

        for attempt in range(max_retries):
            response = self.session.get(url)

            bucket = response.headers.get("X-RateLimit-Bucket", "default")
            self.rate_limit[bucket] = {
                "limit": int(response.headers.get("X-RateLimit-Limit", 0)),
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 0)),
                "reset": int(response.headers.get("X-RateLimit-Reset", 0)),
            }

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 1))
                time.sleep(retry_after)
                continue

            return response

        raise execptions.RateLimitExceeded("Max retries reached due to rate limiting")

    def _post(
        self, path: str, data: dict, max_retries: int = 3
    ) -> dict | requests.Response:
        """
        Post the data to the API with rate limit handling.
        """
        url = f"{self.base_url}{path}"
        for attempt in range(max_retries):
            response = self.session.post(url, json=data)
            bucket = response.headers.get("X-RateLimit-Bucket", "default")
            self.rate_limit[bucket] = {
                "limit": int(response.headers.get("X-RateLimit-Limit", 0)),
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 0)),
                "reset": int(response.headers.get("X-RateLimit-Reset", 0)),
            }
            if response.status_code == 200:
                return response.json()
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 1))
                time.sleep(retry_after)
                continue
            return response
        raise execptions.RateLimitExceeded("Max retries reached due to rate limiting")
