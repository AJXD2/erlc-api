import requests
from erlc.constants import BASE_URL
import erlc.execptions as execptions
import time


class ErlcServerClient:
    def __init__(self, api_key: str, base_url: str = None) -> None:
        self.api_key = api_key
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Server-Key": self.api_key})
        if not self._test_key():
            raise execptions.InvalidApiKey("Invalid API key", client=self)

    def _test_key(self) -> bool:
        """
        Test the API key.
        """
        data = self._get("/server")
        if data.get("code") == 1001:
            return False
        return True

    def _get(self, path: str) -> dict | requests.Response:
        """
        Get the data from the API.
        """
        response = self.session.get(f"{self.base_url}{path}")
        try:
            if response.status_code == 200:
                return response.json()
            if response.status_code == 429:
                data = response.json()
                time.sleep(data.get("retry_after", 0))
                return self._get(path)
        except requests.exceptions.JSONDecodeError:
            pass
        return response
