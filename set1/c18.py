#!/usr/bin/env python
import base64
from shared import ctr_crypt, random_aes_key

def main():
    print("c18")
    ct = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    ct = base64.b64decode(ct)
    pt = ctr_crypt(ct, b"YELLOW SUBMARINE", b"\x00" * 8)
    print("Exercise text decrypted: ")
    print(pt)

    print("--")
    nonce = random_aes_key()[:8]
    print(nonce)
    pt = b"This is an encryption test."
    ct = ctr_crypt(pt, b"BLUE22 SUBMARINE", nonce)
    pt2 = ctr_crypt(ct, b"BLUE22 SUBMARINE", nonce)
    pt3_wrong = ctr_crypt(ct, b"BLUE22 SUBMARINE", random_aes_key()[:8])
    pt4_wrong = ctr_crypt(ct, b"BLUE33 SUBMARINE", random_aes_key()[:8])
    print(f"plaintext: {pt}")
    print(f"Encrypted: {ct}")
    print(f"Decrypted: {pt2}")
    print(f"Decrypted (Wrong Nonce): {pt3_wrong}")
    print(f"Decrypted (Wrong key): {pt4_wrong}")

if __name__ == "__main__":
    main()
