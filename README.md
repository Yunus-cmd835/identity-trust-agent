🛡️ Identity Trust Agent

AI‑powered Trust Evaluator using zk‑KYC, DID, and on‑chain activity — built for the **OnlyFounders AI Hackathon 2025**.

---

## 📌 Project Overview

This agent evaluates the **trustworthiness of an Ethereum wallet** by combining:

| Signal | Source |
|--------|--------|
| 🔗 **On‑chain behavior** | Tx count & unique contract interactions |
| 🧾 **zk‑KYC simulation** | Gitcoin‑Passport style logic |
| 🆔 **DID verification**  | `did:key` method |
| 📜 **Verifiable Credential** | W3C VC with JWS signature |
| ⛓ **On‑chain registry** | VC hash stored on Sepolia |

---

## 🎯 Key Use‑Cases

- DAO access control  
- Web3 recruitment filtering  
- DeFi protocol risk gates  
- KYC‑free community building  

---

## 🖥️ Interfaces

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit agent |
| `dashboard.py` | Visual dashboard & history |
| `agent.py` | Headless agent logic (optional) |

Launch locally:

```bash
pip install -r requirements.txt
streamlit run app.py

🛠️ Tech Stack
Python / Streamlit / Web3.py

W3C Verifiable Credentials, DID:key

zk‑KYC (simulated Gitcoin Passport logic)

Sepolia testnet + Hardhat smart contract

Matplotlib / QR Code / Pillow

🧬 Folder Structure

01_identity_model_agent/
├── app.py
├── dashboard.py
├── agent.py
├── VCRegistryABI.json
├── fetch_onchain.py
├── verify_did.py
├── zk_kyc_checker.py
├── score_calculator.py
├── vc_issuer.py
├── visualizer.py
├── contract_interact.py
├── requirements.txt
├── .gitignore
├── example.env
└── assets/
    ├── credential_qr.png
    └── wallet_analysis.png

🔐 Environment Setup
Copy example.env → .env and fill in your credentials:

PRIVATE_KEY=your_private_key
SEPOLIA_RPC_URL=https://sepolia.alchemy.io/v2/your_project_id
VC_REGISTRY_ADDRESS=0xYourDeployedAddress

.env is ignored by Git (.gitignore)

.

🧪 Sample Evaluation Result

Wallet:            0x99cee6d471907dAaB1805448493104223c848D22
zk-KYC:            ✅ Passed
DID Verified:      ✅ Yes
On-chain Activity: ❌ None
Trust Score:       70 / 100
VC:                Issued & stored on Sepolia

📢 Submission Requirement
GitHub repo — public with this README

Public post tagging

Twitter: @onlyfoundersxyz or

LinkedIn: @Onlyfounders / @MoeIman

✨ Author
Yunus Evangeline • Web3 × AI builder