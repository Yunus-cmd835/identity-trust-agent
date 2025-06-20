import json
import qrcode
from datetime import datetime

def issue_vc(wallet_address, score, risk_level, kyc_passed, did_info):
    vc = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential", "TrustScoreCredential"],
        "issuer": did_info["did"],
        "issuanceDate": datetime.utcnow().isoformat() + "Z",
        "credentialSubject": {
            "id": f"did:ethr:{wallet_address}",
            "wallet": wallet_address,
            "zk_kyc_passed": kyc_passed,
            "score": score,
            "risk_level": risk_level,
            "tx_count": None,
            "contracts_interacted": None,
        },
        "proof": {
            "type": "Ed25519Signature2020",
            "created": datetime.utcnow().isoformat() + "Z",
            "verificationMethod": did_info["verification_method"],
            "proofPurpose": "assertionMethod",
            "jws": "eyJ...simulated...signature...AbCdEf=="
        }
    }

    # ✅ Save VC to file
    with open("credential.json", "w") as f:
        json.dump(vc, f, indent=4)
    print("📜 Verifiable Credential exported to credential.json ✅")

    # ✅ Generate QR code
    vc_json = json.dumps(vc)
    qr = qrcode.make(vc_json)
    qr.save("credential_qr.png")
    print("🔳 QR code saved to credential_qr.png ✅")

    return vc  # ✅ This is the fix
