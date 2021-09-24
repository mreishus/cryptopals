#!/usr/bin/env python
"""
Convert hex to base64

The string:

49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

Should produce:

SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
"""

from shared import hex_string_to_b64_string


def main():
    print("Set 1 / Challenge 1")
    print("Convert hex to base64")
    print("")

    x = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print(f"Input x:  {x}")
    y = hex_string_to_b64_string(x)
    expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    print(f"Output y: {y}")
    print(f"Matches expected? {str(y == expected)}")

if __name__ == "__main__":
    main()
