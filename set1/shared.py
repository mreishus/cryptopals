#/usr/bin/env python

b64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def hex_string_to_b64_string(hex_string):
    hex_bytes = bytes.fromhex(hex_string)
    b64_bytes = hex_bytes_to_b64_bytes(hex_bytes)
    return b64_bytes_to_b64_string(b64_bytes)


def hex_bytes_to_b64_bytes(hex_bytes):
    b64_bytes = bytearray(b"")
    next_b64_byte = 0
    bits_taken = 0

    # Find the individual 1s and 0s in hex_bytes, starting from the left
    for byte in hex_bytes:
        # In this byte, examine the 8 bits from left to right
        for i in range(7, -1, -1):
            mask = 1 << i
            bit = 1 if byte & mask > 0 else 0

            next_b64_byte <<= 1
            next_b64_byte += bit
            bits_taken += 1
            # print(f"bit[{bit}] next_b64_byte[{next_b64_byte}] bits_taken[{bits_taken}]")
            if bits_taken == 6:
                b64_bytes.append(next_b64_byte)
                next_b64_byte = 0
                bits_taken = 0

    # Converting octects (8 bits) to sextets (6 bits) doesn't always line up
    # Sometimes we need to add 0s to fill out the last character
    if bits_taken > 0:
        # We need (6 - bits_taken) more bits: Add 0s
        next_b64_byte <<= (6 - bits_taken)
        b64_bytes.append(next_b64_byte)

    return b64_bytes

def b64_bytes_to_b64_string(b64_bytes):
    output = ""
    parity = 0
    for byte in b64_bytes:
        output += b64_table[byte]
        parity = (parity + 1) % 4

    ## Add padding if needed; we're expected to output in groups of 4 characters
    if parity > 0:
        for _ in range(4 - parity):
            output += "="
    return output
