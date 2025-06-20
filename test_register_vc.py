import json
import os
import hashlib
import time
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Load environment vars
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
ACCOUNT = Web3().eth.account.from_key(PRIVATE_KEY).address

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
print(f"🔗 Connected: {w3.is_connected()}")

# Load ABI
with open("VCRegistryABI.json", "r") as f:
    abi = json.load(f)

# VCRegistry contract address
contract_address = Web3.to_checksum_address("0x81D0aD79857406896eE59d461d057a30368966DA")
contract = w3.eth.contract(address=contract_address, abi=abi)

# Dummy Verifiable Credential
vc_data = {
    "wallet": ACCOUNT,
    "score": 88,
    "timestamp": int(time.time()),
}

# Calculate fake VC hash
vc_json = json.dumps(vc_data, sort_keys=True)
vc_hash = Web3.keccak(text=vc_json)

# Build transaction
tx = contract.functions.registerVC(
    vc_hash, vc_data["score"], vc_data["timestamp"]
).build_transaction({
    "from": ACCOUNT,
    "nonce": w3.eth.get_transaction_count(ACCOUNT),
    "gas": 200000,
    "gasPrice": w3.to_wei("10", "gwei"),
})

# Sign + Send transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print(f"📤 VC Registered! TX Hash: {w3.to_hex(tx_hash)}")
