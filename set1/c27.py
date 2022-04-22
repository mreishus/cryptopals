#!/usr/bin/env python
from shared import pkcs7_pad, random_aes_key, cbc_encrypt, cbc_decrypt, hex_bytes_xor
"""
Challenge 27: Recover the key from CBC with IV=Key
https://cryptopals.com/sets/4/challenges/27
"""

def enc(input_bytes):
    prepend = b"comment1=cooking%20MCs;userdata="
    input_bytes = input_bytes.replace(b";", b"")
    input_bytes = input_bytes.replace(b"=", b"")
    append  = b";comment2=%20like%20a%20pound%20of%20bacon"

    full_bytes = prepend + input_bytes + append
    key = mykey()
    full_bytes = pkcs7_pad(full_bytes, 16)

    # Correct - use a separate IV
    # return cbc_encrypt(full_bytes, key, b"\x00" * 16)
    # Vulnerable - Reuse the Key as the IV
    return cbc_encrypt(full_bytes, key, key)

def dec(encrypted_bytes):
    full_bytes = cbc_decrypt(encrypted_bytes, mykey(), mykey())
    return full_bytes

def is_admin(encrypted_bytes):
    full_bytes = cbc_decrypt(encrypted_bytes, mykey(), mykey())
    print("    (The system has decoded the cipher text: )", full_bytes)
    return b";admin=true;" in full_bytes

def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key

def main():
    print("c27")
    print("I am sending this plaintext to the function:")
    bytes_in = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print(bytes_in)
    ct = enc(bytes_in)
    print("")
    print("I got this encrypted text back: ")
    print(ct)

    print("")
    print("We are splitting the encrypted text into the first three blocks: ")
    b1 = ct[0:16]
    b2 = ct[16:32]
    b3 = ct[32:48]
    print(f"b1[{str(b1)}]\nb2[{str(b2)}]\nb3[{str(b3)}]")
    zeros = b'\x00' * 16

    print("")
    print("Now we are sending this to be decrypted: block1, a block of zeros, block1, block2, block3")
    decrypted = dec(b1 + zeros + b1 + b2 + b3)
    decrypted = dec(b1 + zeros + b1 + b2 + b3)
    p1 = decrypted[0:16]
    p2 = decrypted[16:32]
    p3 = decrypted[32:48]
    print("")
    print(f"Sent ciphertext: [{b1 + zeros + b1 + b2 + b3}]")
    print(f"Got plaintext: [{decrypted}]")
    print("")
    print("Now, if we xor decrypted_block_1 with decrypted_block_3, we can recover the key: ")
    print("Recovered key from plaintext: " + str(hex_bytes_xor(p1, p3)))
    print("Actual key                            : " + str(mykey()))

if __name__ == "__main__":
    main()
