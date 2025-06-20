# agent.py

import streamlit as st
import json
import os
import hashlib
import time
import matplotlib.pyplot as plt
from PIL import Image

# Internal Modules
from fetch_onchain import get_wallet_data
from verify_did import resolve_did
from zk_kyc_checker import check_kyc
from score_calculator import calculate_score
from vc_issuer import issue_vc
from visualizer import visualize_wallet_analysis

# Blockchain
from web3 import Web3
from dotenv import load_dotenv
import asyncio

# Async loop fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Env vars
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("SEPOLIA_RPC_URL")
VC_REGISTRY_ADDRESS = os.getenv("VC_REGISTRY_ADDRESS")

# Web3 setup
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
from_address = account.address

# Load ABI
with open("VCRegistryABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=Web3.to_checksum_address(VC_REGISTRY_ADDRESS), abi=abi)

def register_vc_onchain(vc_hash, score):
    try:
        nonce = w3.eth.get_transaction_count(from_address)
        timestamp = int(time.time())

        tx = contract.functions.registerVC(
            Web3.to_bytes(hexstr=vc_hash),
            int(score),
            timestamp
        ).build_transaction({
            'chainId': 11155111,
            'gas': 250000,
            'gasPrice': w3.to_wei("10", "gwei"),
            'nonce': nonce
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex()
    except Exception as e:
        return f"Error: {str(e)}"

# === UI Starts ===
st.set_page_config(page_title="🛡️ Identity Trust Evaluator", page_icon="🛡️")
st.title("🛡️ Identity Trust Evaluator")
st.markdown("Evaluate wallet trust using on-chain activity, zk-KYC, and DIDs.")

wallet_address = st.text_input("🔗 Wallet Address", "0x99cee6d471907dAaB1805448493104223c848D22")

if st.button("📦 Fetch On-Chain VC"):
    try:
        onchain_vc = contract.functions.getVC(Web3.to_checksum_address(wallet_address)).call()
        vc_hash, score, timestamp = onchain_vc

        st.markdown("### 📦 On-Chain VC Record")
        st.write(f"**VC Hash:** `{vc_hash.hex()}`")
        st.write(f"**Score:** `{score}`")
        st.write(f"**Timestamp:** `{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}`")
    except Exception as e:
        st.error(f"❌ Error fetching VC: {str(e)}")

if st.button("🔍 Evaluate"):
    with st.spinner("Analyzing wallet..."):
        # Step 1: Core fetch
        onchain_data = get_wallet_data(wallet_address)
        did_info = resolve_did(wallet_address)
        kyc_passed = check_kyc(wallet_address)
        score = calculate_score(onchain_data, did_info, kyc_passed)

        risk_level = "low" if score > 75 else "medium" if score > 50 else "high"

        result = {
            "wallet": wallet_address,
            "zk_kyc_passed": kyc_passed,
            "tx_count": onchain_data['tx_count'],
            "unique_contracts_interacted": onchain_data['unique_contracts_interacted'],
            "score": score,
            "risk_level": risk_level,
            "did_info": did_info
        }

        # Step 2: Score Breakdown
        st.markdown("### 🧮 Score Breakdown")
        breakdown = []
        if did_info.get("vc_issued"): breakdown.append("✅ DID Verified: +30")
        else: breakdown.append("❌ DID Not Verified: +0")

        if kyc_passed: breakdown.append("✅ zk‑KYC Passed: +40")
        else: breakdown.append("❌ zk‑KYC Failed: +0")

        if onchain_data["tx_count"] > 0 and onchain_data["unique_contracts_interacted"] > 0:
            breakdown.append("✅ On‑Chain Activity Present: +30")
        else:
            breakdown.append("❌ No On‑Chain Activity: +0")

        for b in breakdown:
            st.markdown(f"- {b}")
        st.markdown(f"🏁 **Total Score:** `{score}` → Risk: **{risk_level.upper()}**")

        # Step 3: Show & Save JSON
        st.success("✅ Final Evaluation")
        st.json(result)

        with open("output.json", "w") as f:
            json.dump(result, f, indent=4)
        st.download_button("📁 Download output.json", data=json.dumps(result, indent=4), file_name="output.json")

        # Step 4: Chart
        st.markdown("### 📊 Trust Score Chart")
        fig, ax = plt.subplots()
        bars = ax.bar(["Trust Score"], [score], color="green" if score > 75 else "orange" if score > 50 else "red")
        ax.set_ylim(0, 100)
        ax.bar_label(bars)
        st.pyplot(fig)

        # Step 5: VC Issuing
        vc_obj = issue_vc(wallet_address, score, risk_level, kyc_passed, did_info)
        if vc_obj:
            st.markdown("### 📜 Verifiable Credential Issued")
            st.download_button("📥 Download credential.json", data=json.dumps(vc_obj, indent=4), file_name="credential.json")

            jws = vc_obj.get("proof", {}).get("jws")
            if jws:
                st.markdown("#### 🔏 JWS Signature")
                st.code(jws, language="text")

            vc_hash = hashlib.sha256(json.dumps(vc_obj).encode()).hexdigest()
            st.markdown(f"**VC Hash:** `0x{vc_hash}`")

            st.markdown("### ⛓ Registering on-chain…")
            tx_hash = register_vc_onchain(f"0x{vc_hash}", score)
            st.markdown(f"🧾 **Transaction Hash:** `{tx_hash}`")

            if not tx_hash.startswith("Error"):
                st.markdown(f"[🔗 View on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash})")

            st.success("🎯 Credential Registered Successfully!")
            st.balloons()

        # Step 6: Visualizer Chart
        visualize_wallet_analysis(onchain_data['tx_count'], onchain_data['unique_contracts_interacted'], risk_level)
        if os.path.exists("wallet_analysis.png"):
            st.image("wallet_analysis.png", caption="📊 Wallet Risk Profile", use_container_width=True)
