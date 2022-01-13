#!/usr/bin/env python
from mt_rng import MTRNG
import random
import time

## y   = 11011010
## y>>4      1101
## XOR ----------
##           0111
##       11010111

def untemper(y):
    w = 32 # word size (bits)
    (s, b) = (7, 0x9D2C5680)  # TGFSR(R) Tempering bit shift + mask
    (t, c) = (15, 0xEFC60000) # TGFSR(R) Tempering bit shift + mask
    (u, d) = (11, 0xFFFFFFFF) # additional Mersenne Twister tempering bit shifts/masks
    l = 18 # additional Mersenne Twister tempering bit shifts/masks

    print('--untemper--')
    print(f"before: {y} {y:32b} ")

    # undo this: y = y ^ (y >> self.l)        # (self.l is 18)
    # step3 : 2333914319 10001011000111001011010011001111
    #                    |-----18---------||------14----|
    # Iermed: 8903                         10001011000111
    # step4 : 2333906440 10001011000111001001011000001000
    # The first 18 digits are the same.
    y = inverse_xor_right_shift(y, l)
    print(f"undo1 : {y} {y:32b} ")
    y = 3360862799
    print(f"force : {y} {y:32b} ")

    # undo this: y = y ^ (y >> 11)        
    #before: 3360406328 11001000010010111011101100111000 
    #                   |---11----||---11----|
    #                              110010000100101110111
    #      ---------------------------------------------
    #step1 : 3360862799 11001000010100101011001001001111
    # The first 11 digits are the same.
    y = inverse_xor_right_shift(y, 11)
    print(f"undo2 : {y} {y:32b} ")



def inverse_xor_right_shift(y, l):
    w = 32
    output = 0
    shifted = (y >> l)

    # i = [31 - 14], or the first 18 digits that are unchanged
    for i in range(w - 1, (w - l) - 1, -1):
        digit = (y >> i) & 1
        output *= 2
        output += digit
    # print(f"after : {output}       {output:32b} ")
    # print(f"shift : {shifted}    {shifted:32b} ")
    # i = [13 - 0], or the next 14 digits that are changed
    for i in range((w-l) - 1, 0-1, -1):
        # print(i, (w - 2*l), end=" ")
        digit = (y >> i) & 1
        shifted_digit = (shifted >> i) & 1

        # If this is the case, we've run out of data,
        # and need to start looking in our generated output for XOR digits
        # This is really hard to understand/explain :/
        if i < w - 2*l:
            shifted_digit = (output >> (w - 2*l)) & 1
        # print(f" | {shifted_digit} | {output:>42b}")

        output *= 2
        output += digit ^ shifted_digit
    # print(f"after : {output} {output:32b} ")
    # print(f"shifted     : {shifted} {shifted:32b} ")
    return output



def main():
    r = MTRNG()
    print('hi')
    r.seed_mt(100)
    num = r.extract_number()
    print(num)
    untemper(num)


if __name__ == "__main__":
    main()
