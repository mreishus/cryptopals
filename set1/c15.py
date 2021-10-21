#!/usr/bin/env python
from shared import pkcs7_pad, is_pkcs7_pad_valid

def main():
    print("c15")
    padded_valid1 = pkcs7_pad(b"ICE ICE BABY", 16)
    padded_valid2 = b"ICE ICE BABY\x04\x04\x04\x04"
    padded_invalid1 = b"ICE ICE BABY\x05\x05\x05\x05"
    padded_invalid2 = b"ICE ICE BABY\x01\x02\x03\x04"
    z = is_pkcs7_pad_valid(padded_valid1, 16)
    print(z)
    z = is_pkcs7_pad_valid(padded_valid2, 16)
    print(z)
    z = is_pkcs7_pad_valid(padded_invalid1, 16)
    print(z)
    z = is_pkcs7_pad_valid(padded_invalid2, 16)
    print(z)
    # z = is_pkcs7_pad_valid(padded_invalid1, 16)

if __name__ == "__main__":
    main()
