# score_calculator.py

def calculate_score(onchain_data: dict, did_info: dict, kyc_passed: bool) -> float:
    """
    Calculate a trust score based on on-chain data, DID credentials, and zk-KYC status.

    Weights:
    - zk-KYC: 40 pts
    - Verifiable Credential (VC): 20 pts
    - Transaction count: max 20 pts (0.1 pt per tx, capped at 200 txs)
    - Unique contract interactions: max 20 pts (2 pts each, capped at 10)
    - Risky contract interaction: -10 pts

    Returns:
        A float score between 0 and 100.
    """
    score = 0

    # ✅ KYC & VC-based trust
    score += 40 if kyc_passed else 0
    score += 20 if did_info.get("vc_issued") else 0

    # ✅ On-chain activity
    tx_points = min(onchain_data.get("tx_count", 0) / 10, 20)
    contract_points = min(onchain_data.get("unique_contracts_interacted", 0) * 2, 20)
    score += tx_points + contract_points

    # ⚠️ Penalty for risky interactions
    if onchain_data.get("interacted_with_risky_contract", False):
        print("⚠️ Wallet interacted with risky contract. -10 pts")
        score -= 10

    return round(min(max(score, 0), 100), 1)  # Clamp to [0, 100]
