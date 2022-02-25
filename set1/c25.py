#!/usr/bin/env python
import base64

from shared import ecb_decrypt, ecb_encrypt, random_aes_key, ctr_crypt, ctr_crypt2, random_bytes, hex_bytes_xor, ctr_keystream
from itertools import islice


def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def get_plaintext():
    data = get_data("./25.txt")
    source_b64 = "".join(data)
    source_bytes = base64.b64decode(source_b64)

    key_ascii = "YELLOW SUBMARINE"
    key_bytes = str.encode(key_ascii)

    plaintext_bytes = ecb_decrypt(source_bytes, key_bytes)
    return plaintext_bytes

def edit(ciphertext, key_bytes, nonce_bytes, offset, newtext):
    """
    Now, write the code that allows you to "seek" into the ciphertext, decrypt, and
    re-encrypt with different plaintext.
    """
    keystream_bytes = list(islice(ctr_keystream(key_bytes, nonce_bytes), offset, offset + len(newtext)))
    newtext_encrypted = hex_bytes_xor(newtext, keystream_bytes)
    return ciphertext[:offset] + newtext_encrypted + ciphertext[offset + len(newtext):]


def verify_ctr_crypt2():
    pt = get_plaintext()
    key = random_aes_key()
    nonce = random_bytes(8)
    ct = ctr_crypt(pt, key, nonce)
    ct2 = ctr_crypt2(pt, key, nonce)
    print("Do ctr_crypt and ctr_crypt2 behave the same?")
    print(ct == ct2)

def verify_edit():
    pt = get_plaintext()

    # encrypt under CTR with a random key (for this exercise the key should be
    # unknown to you, but hold on to it).
    key = random_aes_key()
    nonce = random_bytes(8)
    ct = ctr_crypt(pt, key, nonce)
    ct2 = edit(ct, key, nonce, 20, b"AAAAAABBBBBB")
    pt = ctr_crypt(ct2, key, nonce)
    print(pt)



def main():
    pt = get_plaintext()

    # encrypt under CTR with a random key (for this exercise the key should be
    # unknown to you, but hold on to it).
    key = random_aes_key()
    nonce = random_bytes(8)
    ct = ctr_crypt(pt, key, nonce)

    # Imagine the "edit" function was exposed to attackers by means of an API
    # call that didn't reveal the key or the original plaintext; the attacker
    # has the ciphertext and controls the offset and "new text".
    # Recover the original plaintext. 
    recovered_keystream = bytearray()
    for i in range(len(ct)):
        ct2 = edit(ct, key, nonce, i, b"A")
        keystream_guess = int.from_bytes(b"A", "little") ^ ct2[i]
        keystream_byte = keystream_guess.to_bytes(1, "big")
        recovered_keystream.extend(keystream_byte)
    print("Recovered ciphertext:")
    print(hex_bytes_xor(recovered_keystream, ct))

if __name__ == "__main__":
    main()
