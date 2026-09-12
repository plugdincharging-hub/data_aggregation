from datetime import datetime, timedelta, timezone
import requests as r

def data_retrieval(key: str):
    thirty_days_ago = int(
        (datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
    
    list_of_payments = []
    params = {
        "limit": 100,
        "created[gte]": thirty_days_ago}

    while True:
        intent_response = r.get("https://api.stripe.com/v1/payment_intents",
        auth=(key, ""),
        params=params,
        timeout=30
        )
        intent_response.raise_for_status()
        page = intent_response.json()

        list_of_payments.extend(page["data"])

        if not page["has_more"]:
            return list_of_payments

        params["starting_after"] = page["data"][-1]["id"]

def fee_retrieval(charge_id: str, key: str):
    '''Gather transaction ID to work out stripe fee'''

    transaction_response = r.get(f"https://api.stripe.com/v1/charges/{charge_id}",
    auth=(key, "")
    )
    transaction_response.raise_for_status()

    transaction_id  = transaction_response.json()["balance_transaction"]

    fee_value = r.get(f"https://api.stripe.com/v1/balance_transactions/{transaction_id }",
    auth=(key, "")
    )
    fee_value = fee_value.json()["fee"]

    return fee_value

def retrieve_non_returns(api_key: str, list_of_payments: list):

    thirty_days_ago = int(
        (datetime.now(timezone.utc) - timedelta(days=30)).timestamp())

    params = {
        "created[gte]": thirty_days_ago
    }

    while True:
        response = r.get(
            f"https://api.stripe.com/v1/payment_intents",
            auth=(api_key, ""),
            params=params,
            timeout=30)

        response.raise_for_status()

        page = response.json()

        list_of_payments.extend(page["data"])

        if not page["has_more"]:
            return list_of_payments

        params["starting_after"] = page["data"][-1]["id"]
