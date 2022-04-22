#!/usr/bin/env python
from pure_python_crypto import sha1_compress, SHA1, md_pad_64, big_endian_bytes
from shared import random_aes_key
import random

""" Break a SHA-1 keyed MAC using length extension """


def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random.choice(list(open("/usr/share/dict/words"))).strip()
        ## Convert to bytes
        mykey.key = mykey.key.encode("utf-8")
    return mykey.key


def generate_mac(message):
    """a secret-prefix MAC: SHA1(key || message)"""
    key = mykey()
    # return sha1(key + message)
    return bytes(SHA1(key + message))


def verify(message, mac):
    want_mac = generate_mac(message)
    # print(f"want_mac = {want_mac}")
    # print(f"mac {mac}")
    return want_mac == mac


def pad(message, fake_byte_len=None):
    "computes the MD padding of an arbitrary message: Same as SHA1"
    length_to_bytes = lambda length: big_endian_bytes([length], 8)
    return md_pad_64(message, length_to_bytes, fake_byte_len)


def main():
    print("c29")
    print("")

    orig_pt = (
        b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    )
    mac = generate_mac(orig_pt).hex()

    # Split sha1 into 5 sections of 8 hex characters, convert to decimal
    # "741daf73"  "a7a4c52b"   dbe018c5 228ab599 1a172cff
    # 1948102515   2812593451

    a = int(mac[0:8], 16)
    b = int(mac[8:16], 16)
    c = int(mac[16:24], 16)
    d = int(mac[24:32], 16)
    e = int(mac[32:48], 16)
    print(f"original phrase = {orig_pt}")
    print("")
    print("Got key from mykey(), generated mac of sha1(key + message)")
    print(f"mac       = {mac}")
    print("")
    print("Split sha1 into 5 sections of 8 hex characters, convert to decimal")
    print("a,b,c,d,e = ", end="")
    print(a, b, c, d, e)
    print("We will use these values as internal state of SHA1 in our extension attack")

    print("")
    add_this = b";admin=true"
    print(f"We want to add this phrase to the end of the message: {add_this}")
    print("")

    print(
        "We don't know how long the secret key is, so we need to guess several values: "
    )
    for keylen in range(20):
        print(f"Guessing keylen={keylen}...")

        ## As a placeholder for the key, prepend a number of "A"s to the message
        orig_with_fake_key = (b"A" * keylen) + orig_pt
        ## That allows us to compute the sha1 padding of the message
        padded_orig_with_fake_key = pad(orig_with_fake_key)
        ## The length of this would be the internal state length of SHA1 when it was done
        fake_len_so_far = len(padded_orig_with_fake_key)
        ## We already have the register state: A, B, C, D, E

        ## The message we will be forging includes the padding. This is the tricky part.
        ## Take the result of pad(fake_key + orig_message), then remove the fake key at the beginning,
        ## and add our message
        forged_message = padded_orig_with_fake_key[keylen:] + add_this
        ## Generate the forged mac by only SHA1 encoding what we want to add, but providing the internal state
        ## that we computed earlier.
        forged_mac = bytes(
            SHA1(
                add_this,
                state=[a, b, c, d, e],
                fake_byte_len=fake_len_so_far + len(add_this),
            )
        )

        if verify(forged_message, forged_mac):
            print("")
            print(" ---> SUCCESS! ")
            print(
                " We were able to forge the message and mac pair, without knowing the secret key: "
            )
            print(f"  forged_message=[{forged_message}]")
            print(f"  forged_mac=[{forged_mac.hex()}]")
            print("The validation system accepted this as a valid message+mac pair!")
            print("")
            break
    exit()


if __name__ == "__main__":
    main()
