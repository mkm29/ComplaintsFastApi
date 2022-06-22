import asyncio
from typing import Optional

import aiohttp
import requests
from fastapi import HTTPException

from app import settings
from app.models.enums import CurrencyType
from app.utils.helpers import fetch, post


class WiseService:
    def __init__(self):
        self.base_url = settings.wise_url
        api_key = settings.wise_api_key
        if not self.base_url or not api_key:
            raise HTTPException(400, "API Key or Wise URL not found")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
        }
        # self.profile_id = self._get_profile_id()

    async def get_profile_id(self) -> Optional[int]:
        """
        Get the profile ID that is associated with the given API key

        @raises an HTTPException if the status code of the response is not 2xx

        @returns: the ID associated with your Wise API key
        """
        url = f"{self.base_url}/v2/profiles"
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url, headers=self.headers)
        if response.status_code != 200:
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
        return response["id"]

    def create_recipient_account(
        self, full_name: str, currency_type: CurrencyType, iban: str
    ) -> Optional[int]:
        """
        Create an account for a recipient (for receiving funds)

        @param full_name: The full name of the complainer (get this from the db)
        @type full_name: str
        @param currency_type: The currency type (USD) to send
        @type currency_type: str
        @param iban: IBAN number to receive funds
        @type iban: str
        @raises an HTTPException if the status code of the response is not 2xx

        @returns: account ID of created recipient
        """
        url = f"{self.base_url}/v1/accounts"
        data = {
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "currency": currency_type.value,
            "type": "iban",
            "details": {"legalType": "PRIVATE", "IBAN": iban},
        }
        response = requests.post(url, headers=self.headers, json=data)
        if not response.ok:
            raise HTTPException(
                response.status_code, "Error creating recipient account"
            )
        return response["id"]

    def create_transfer(self, recipient_id: int) -> Optional[int]:
        """
        Transfer some funds

        @param recipient_id: The full name of the complainer (get this from the db)
        @type recipient_id: int
        @raises an HTTPException if the status code of the response is not 2xx

        @returns: ID of transfer
        """
        url = f"{self.base_url}/v1/transfers"
        data = {
            "targetAccount": recipient_id,
            "quoteUuid": "",
            "customerTransactionId": "<the unique identifier you generated for the transfer attempt>",
            "details": {
                "reference": "to my friend",
                "transferPurpose": "verification.transfers.purpose.pay.bills",
                "transferPurposeSubTransferPurpose": "verification.sub.transfers.purpose.pay.interpretation.service",
                "sourceOfFunds": "verification.source.of.funds.other",
            },
        }


if __name__ == "__main__":

    async def main():
        wise = WiseService()
        await wise.get_profile_id()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    a = 5
