# verify_did.py

"""
Resolves a static Decentralized Identifier (DID) and Verifiable Credential (VC) info.

Note:
This bypasses didkit-based generation (which causes event loop errors on Windows).
Pre-generated DID from Linux can be replaced when dynamic DIDKit support is added.
"""

def resolve_did(_wallet_address: str) -> dict:
    """
    Return a dictionary with static DID details and VC issuance status.

    Args:
        _wallet_address (str): Wallet address (unused in static mode)

    Returns:
        dict: DID, verification method, and VC status.
    """
    did = "did:key:z6Mkr7AQExaFpEomuhBbi1pjpEvy2YbWoFSDovro2jCNfkTh"
    
    return {
        "did": did,
        "verification_method": f"{did}#{did.split(':')[-1]}",
        "vc_issued": True
    }
