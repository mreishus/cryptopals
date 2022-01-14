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

    # print('--untemper--')
    # print(f"before: {y} {y:32b} ")
    y = inverse_xor_right_shift(y, l)
    y = inverse_xor_left_shift(y, t, c)
    y = inverse_xor_left_shift(y, s, b)
    y = inverse_xor_right_shift(y, u)
    # print(f"after : {y}    {y:32b} ")
    return y


def inverse_xor_left_shift(y, shift_amount, shift_mask):
    w = 32
    output = 0
    shifted = y << shift_amount
    for i in range(w):
        # Grab the digit in the ith place of the "self.c" mask
        mask_digit = shift_mask & (1 << i)
        mask_digit = 1 if mask_digit > 0 else 0
        xor_digit = 'dunno'

        y_digit = y & (1 << i)
        y_digit = 1 if y_digit > 0 else 0
        if mask_digit == 0:
            # if 0, there's no xOR to do, let the i'th digit of Y take hold
            digit = y_digit
        else:
            # if 1, we need to XOR with the shifted version:

            if i > ((2 * shift_amount) - 1):
                # In some cases we need to rebuld shifted with the latest
                # information we've already computed
                shifted = output << shift_amount
            xor_digit = shifted & (1 << i)
            xor_digit = 1 if xor_digit > 0 else 0
            digit = y_digit ^ xor_digit

        output |= digit * 2 ** i
    return output


def inverse_xor_right_shift(y, l):
    # undo this: y = y ^ (y >> self.l)        # (self.l is 18)
    # step3 : 2333914319 10001011000111001011010011001111
    #                    |-----18---------||------14----|
    # Iermed: 8903                         10001011000111
    # step4 : 2333906440 10001011000111001001011000001000
    # The first 18 digits are the same.

    ## undo this: y = y ^ (y >> 11)        
    ##before: 3360406328 11001000010010111011101100111000 
    ##                   |---11----||---11----|
    ##                              110010000100101110111
    ##      ---------------------------------------------
    ##step1 : 3360862799 11001000010100101011001001001111
    ## The first 11 digits are the same.
    #y = inverse_xor_right_shift(y, 11)
    #print(f"undo2 : {y} {y:32b} ")
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
    print(untemper(num))


if __name__ == "__main__":
    main()
