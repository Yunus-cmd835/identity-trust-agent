from web3 import Web3
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# ✅ Load values from .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("VC_REGISTRY_ADDRESS")

# ✅ Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
from_address = account.address

# ✅ Load contract ABI
with open("VCRegistryABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

def register_vc(vc_hash: str, score: int):
    nonce = w3.eth.get_transaction_count(from_address)
    timestamp = int(time.time())

    txn = contract.functions.registerVC(vc_hash, score, timestamp).build_transaction({
        'chainId': 11155111,  # Sepolia Chain ID
        'gas': 250000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"✅ Tx sent! Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("🎉 VC Registered Successfully:", receipt)

# 🧪 Example usage
if __name__ == "__main__":
    register_vc("0xabc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abcd", 82)
