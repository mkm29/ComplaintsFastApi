from typing import Optional

import requests
from fastapi import HTTPException

from app import settings


class WiseService:
    def __init__(self):
        self.base_url = settings.wise_url
        api_key = settings.wise_api_key
        if not self.base_url or not api_key:
            raise HTTPException(400, "API Key or Wise URL not found")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self) -> Optional[int]:
        """
        Get the profile ID that is associated with the given API key

        @raises an HTTPException if the status code of the response is not 2xx

        @returns: the ID associated with your Wise API key
        """
        url = f"{self.base_url}/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if not response.ok:
            raise HTTPException(response.status_code, "Error getting ID from Wise")
        # response.json() will be a list
        ids = [item["id"] for item in response.json() if item["type"] == "PERSONAL"]
        if not ids:
            raise HTTPException(400, "No account of type PERSONAL found")
        return ids[0]

    def create_quote(self, amount: float):
        """
        Create a quote of a given amount and currency

        @param amount: The amount to send
        @type amount: float
        @raises an HTTPException if the status code of the response is not 2xx

        @returns:
        """
        url = f"{self.base_url}/v3/profiles/{self.profile_id}/quotes"
        data = {
            "sourceCurrency": "USD",
            "targetCurrency": "USD",
            "sourceAmount": amount,
        }
        response = requests.post(url, headers=self.headers, json=data)
        if not response.ok:
            raise HTTPException(response.status_code, "Error creating quote")
        response = {
            "feePercentage": [
                payment["feePercentage"] for payment in response["paymentOptions"]
            ],
            "estimatedDelivery": [
                payment["estimatedDelivery"] for payment in response["paymentOptions"]
            ],
            "targetAmount": [
                payment["targetAmount"] for payment in response["paymentOptions"]
            ],
            "targetCurrency": [
                payment["targetCurrency"] for payment in response["paymentOptions"]
            ],
            "status": response["status"],
            "id": response["id"],
        }
        return response
