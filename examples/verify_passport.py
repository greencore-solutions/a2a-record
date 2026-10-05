"""A2A Passport — verify a passport offline: the document and the key over plain HTTP, the signature checked here.
pip install requests cryptography
usage: python verify_passport.py [passport_id]
"""
import sys, json, base64, requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

BASE = "https://a2a-passport.ai"
pid = sys.argv[1] if len(sys.argv) > 1 else "gtin-03284230006408"
unb = lambda s: base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()

doc = requests.get(f"{BASE}/passport/{pid}.json", timeout=60).json()
keys = requests.get(f"{BASE}/.well-known/jwks.json", timeout=60).json()["keys"]
sig = doc["signature"]
key = next(k for k in keys if k["kid"] == sig["kid"])
header, _, signature = sig["jws"].split(".")
canonical = json.dumps({k: v for k, v in doc.items() if k != "signature"}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
Ed25519PublicKey.from_public_bytes(unb(key["x"])).verify(unb(signature), (header + "." + b64(canonical)).encode("ascii"))  # raises if the signature is not valid
print("valid:", doc["passport_id"], "version", doc["version"], "issued", doc["issued_at"], "key id", sig["kid"])
