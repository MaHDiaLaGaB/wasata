import requests
from app.core.config import config
import json


class TlyncClient:
    def __init__(self, is_test_environment=True):
        self.test_url = config.TLYNC_TEST_BASE_URL
        self.live_url = config.TLYNC_BASE_URL
        self.base_url = self.test_url if is_test_environment else self.live_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.token = config.TLYNC_TOKEN

    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"

    def handle_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            else:  # POST request
                response = requests.post(url, data=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": str(err), "response": err.response.json()}

    def initiate_payment(self, store_id, amount, phone, backend_url, frontend_url, custom_ref):
        data = {
            "id": store_id,
            "amount": amount,
            "phone": phone,
            "backend_url": backend_url,
            "frontend_url": frontend_url,
            "custom_ref": custom_ref
        }
        return self.handle_request("POST", "payment/initiate", data)

    def get_transaction_receipt(self, store_id, transaction_ref, custom_ref):
        data = {
            "store_id": store_id,
            "transaction_ref": transaction_ref,
            "custom_ref": custom_ref
        }
        return self.handle_request("POST", "receipt/transaction", data)


# Usage example
# api_client = TLYNCPaymentAPI(is_test_environment=True)
# api_client.set_token("your-access-token-here")
# response = api_client.initiate_payment("store-id", 100.0, "123456789", "test@example.com", "http://backend.url",
#                                        "http://frontend.url", "custom-ref")
# print(response)
