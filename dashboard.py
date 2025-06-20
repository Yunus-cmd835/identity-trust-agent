import streamlit as st
import json
import os
from fetch_onchain import get_wallet_data
from verify_did import resolve_did
from zk_kyc_checker import check_kyc
from score_calculator import calculate_score
from vc_issuer import issue_vc
from visualizer import visualize_wallet_analysis

st.set_page_config(page_title="🔐 Identity Trust Dashboard", layout="wide")

st.title("📊 Identity Trust Dashboard")

wallet = st.text_input("🔗 Wallet Address", "0x99cee6d471907dAaB1805448493104223c848D22")

HISTORY_FILE = "history.json"

# ✅ Load history if it exists
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# ✅ Save current result to history
def save_to_history(entry):
    history = load_history()
    history.insert(0, entry)  # newest first
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ✅ Clear full history
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# ✅ Evaluate Wallet Section
if st.button("🔍 Evaluate Wallet"):
    onchain = get_wallet_data(wallet)
    did_info = resolve_did(wallet)
    kyc = check_kyc(wallet)
    score = calculate_score(onchain, did_info, kyc)

    result = {
        "wallet": wallet,
        "zk_kyc_passed": kyc,
        "tx_count": onchain["tx_count"],
        "unique_contracts_interacted": onchain["unique_contracts_interacted"],
        "interacted_with_risky_contract": onchain["interacted_with_risky_contract"],
        "score": score,
        "risk_level": "low" if score > 75 else "medium" if score > 50 else "high",
        "did_info": did_info
    }

    # ✅ Save to history
    save_to_history(result)

    st.subheader("✅ Final Evaluation")
    st.json(result)

    st.markdown("---")
    st.subheader("🧠 On‑Chain Analysis")
    st.write(f"🔸 Transaction Count: **{onchain['tx_count']}**")
    st.write(f"🔸 Unique Contracts: **{onchain['unique_contracts_interacted']}**")
    if onchain["interacted_with_risky_contract"]:
        st.error("⚠️ Interacted with risky contract!")

    st.subheader("🔐 DID & zk‑KYC")
    st.write(f"🆔 DID: `{did_info['did']}`")
    st.success("✅ zk‑KYC passed" if kyc else "❌ zk‑KYC failed")

    st.subheader("📊 Trust Score")
    st.write(f"🔢 Score: **{score}**")
    st.write(f"⚠️ Risk Level: **{result['risk_level'].upper()}**")

    st.markdown("---")
    st.subheader("📈 Visualization")
    visualize_wallet_analysis(onchain["tx_count"], onchain["unique_contracts_interacted"], result["risk_level"])
    st.image("wallet_analysis.png", caption="Trust Analysis Chart", use_column_width=True)

    st.markdown("---")
    st.subheader("📜 Verifiable Credential")
    vc = issue_vc(wallet, score, result["risk_level"], kyc, did_info)
    st.download_button("📥 Download credential.json", data=json.dumps(vc, indent=4), file_name="credential.json")
    st.image("credential_qr.png", caption="VC QR Code", use_column_width=False)

# ✅ Evaluation History Section
st.markdown("---")
st.subheader("📚 Evaluation History")

history = load_history()

col1, col2 = st.columns([3, 1])
with col1:
    if history:
        for i, item in enumerate(history[:5]):  # show latest 5
            with st.expander(f"🧾 {item['wallet']} | Score: {item['score']} | Risk: {item['risk_level'].upper()}"):
                st.json(item)
    else:
        st.info("No previous evaluations found.")

with col2:
    if st.button("🧹 Clear History"):
        clear_history()
        st.success("History cleared!")
