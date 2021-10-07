#!/usr/bin/env python
"""
Implement CBC mode

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized
messages, despite the fact that a block cipher natively only transforms
individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before
the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block,
is added to a "fake 0th ciphertext block" called the initialization vector, or
IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, making
it encrypt instead of decrypt (verify this by decrypting whatever you encrypt
to test), and using your XOR function from the previous exercise to combine
them.

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW
SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.

Do not use OpenSSL's CBC code to do CBC mode, even to verify your results.
What's the point of even doing this stuff if you aren't going to learn from it?

https://www.youtube.com/watch?v=0abs6qfuLpg
^^ Modes of operation: ECB vs CBC vs others

"""
import base64
from shared import pkcs7_pad, hex_bytes_xor, ecb_encrypt, ecb_decrypt


def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main():
    key_ascii = "YELLOW SUBMARINE"
    key_bytes = str.encode(key_ascii)

    data = get_data("10.txt")
    source_b64 = "".join(data)
    source_bytes = base64.b64decode(source_b64)

    bs = 16  # block_size
    iv = b"\x00" * bs
    prev = iv
    decrypted = bytearray()
    for block in chunks(source_bytes, bs):
        block = pkcs7_pad(block, bs)
        output1 = ecb_decrypt(block, key_bytes)
        output2 = hex_bytes_xor(output1, prev)
        # print("--")
        # print(f"block           {block}")
        # print(f"decrypted       {output1}")
        # print(f"decrypted+xored {output2}")
        decrypted.extend(output2)
        prev = block
    print(decrypted)


if __name__ == "__main__":
    main()
