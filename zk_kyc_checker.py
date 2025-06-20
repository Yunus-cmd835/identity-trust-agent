# zk_kyc_checker.py

def check_kyc(wallet_address):
    """
    Simulates a Gitcoin Passport zk-KYC score based on wallet pattern.
    You can tweak logic to test different scoring conditions.
    """
    # Sample simulation logic (make it smarter if needed)
    trusted_wallets = [
        "0x99cee6d471907dAaB1805448493104223c848D22",
        "0x1234567890abcdef1234567890abcdef12345678",
        "0x2d0d0af8ef7ea5021385a7c725aa8e4df1111e96",
    ]

    if wallet_address.lower() in [addr.lower() for addr in trusted_wallets]:
        print("✅ Simulated zk-KYC passed")
        return True
    else:
        print("❌ Simulated zk-KYC failed")
        return False

