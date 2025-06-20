# fetch_onchain.py

import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_data(wallet_address):
    base_url = "https://api.etherscan.io/api"

    tx_resp = requests.get(base_url, params={
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    })

    print("📡 Etherscan raw response:", tx_resp.text)

    try:
        txs = tx_resp.json().get("result", [])
    except Exception as e:
        print("❌ Error parsing response:", e)
        return {
            "tx_count": 0,
            "unique_contracts_interacted": 0,
            "interacted_with_risky_contract": False
        }

    if not isinstance(txs, list):
        print("⚠️ Unexpected txs format:", txs)
        return {
            "tx_count": 0,
            "unique_contracts_interacted": 0,
            "interacted_with_risky_contract": False
        }

    contracts = set()
    risky = load_risky_contracts()
    interacted_risky = False

    for tx in txs:
        to_address = tx.get("to")
        if to_address:
            to_address = to_address.lower()
            contracts.add(to_address)
            if to_address in risky:
                interacted_risky = True

    return {
        "tx_count": len(txs),
        "unique_contracts_interacted": len(contracts),
        "interacted_with_risky_contract": interacted_risky
    }

def load_risky_contracts():
    try:
        with open("risky_contracts.json", "r") as f:
            return set(addr.lower() for addr in json.load(f))
    except Exception as e:
        print("⚠️ Could not load risky contracts:", e)
        return set()
