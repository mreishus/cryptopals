#!/usr/bin/env python
import random
from shared import pkcs7_pad, pkcs7_unpad, random_aes_key, cbc_encrypt, cbc_decrypt


def get_rand_string():
    strings = [
        b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
    ]
    random_i = random.randrange(len(strings))
    return b"YELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINE"
    return b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    return strings[random_i]


def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key


def f1():
    """ Select random string -> Pad it -> Return CBC encrypted version and IV """
    s = get_rand_string()
    s = pkcs7_pad(s, 16)
    iv = random_aes_key()
    ct = cbc_encrypt(s, mykey(), iv)
    return ct, iv


def f2(ct, iv):
    """Consume the ciphertext produced by the first function, decrypt it,
    check its padding, and return true or false depending on whether the
    padding is valid."""
    pt = cbc_decrypt(ct, mykey(), iv)
    # print(f"      ---> shh: decrypted to [{pt[-17:]}]")
    try:
        pt = pkcs7_unpad(pt, 16)
    except Exception:
        return False
    return True


def main():
    print("c17")
    ct, iv = f1()
    print("Server gave me this cipher text:")
    print(ct)
    print("Server gave me this IV:")
    print(iv)

    print("")
    print("[Original] Is the padding valid?")
    pt = f2(ct, iv)
    print(pt)

    # 5 blocks: ct 0-79. To edit last char, change [63] or [-17] or [79 - 16]
    # 4 blocks: ct 0-63. To edit last char, change [47] or [-17] or [63 - 16]
    # 3 blocks: ct 0-47. To edit last char, change [31] or [-17] or [47 - 16]
    # guess = ord('=')
    # print(guess)
    # # mod_ct[-17] = 0
    # print(mod_ct[-17])
    # for i in range(len(mod_ct)):
    #     print(f"{i} {mod_ct[i]}")
    # print(f"Len = {len(mod_ct)}")

    mod_ct = bytearray(ct)
    answer = bytearray(len(ct))

    # guess_index = len(mod_ct) - 1
    for guess_index in range(len(ct) - 1, -1, -1):
        found_guess = False
        modify_index = guess_index - 16
        target_pad = 16 - (guess_index % 16)

        # If we're guessing stuff in the second to last block, we no longer need the last block
        distance = len(ct) - guess_index
        blocks_to_discard = (distance - 1) // 16

        print(f"GUESS INDEX: [{guess_index}] MODIFY INDEX: [{modify_index}] || Target Pad [{target_pad}] || Blocks to discard [{blocks_to_discard}] ")
        if modify_index < 0:
            break

        for guess in range(256):
            if guess == 1:
                continue
            mod_ct = bytearray(ct)
            # print(f"Changing {modify_index}")
            mod_ct[modify_index] ^= guess ^ target_pad
            for j in range(target_pad):
                if j == 0:
                    continue
                # print(f"Changing {modify_index + j}")
                mod_ct[modify_index + j] ^= answer[guess_index + j] ^ target_pad

            # print("Mod ct before discarding: ", len(mod_ct))
            if (blocks_to_discard > 0):
                for i in range(blocks_to_discard):
                    mod_ct = mod_ct[0:-16]
                # print("Mod ct after discarding: ", len(mod_ct))

            valid_padding = f2(mod_ct, iv)
            # print(f"{guess} {valid_padding}")
            if valid_padding:
                print(f"Guess is: {guess}")
                answer[guess_index] = guess
                found_guess = True
                break
        if not found_guess:
            print("Could not find guess..")
            break
    print(answer)


    print("")
    print("[Modified] Is the padding valid?")
    ct = bytes(mod_ct)
    print(pt)


if __name__ == "__main__":
    main()
