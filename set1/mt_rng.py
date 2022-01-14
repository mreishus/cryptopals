#!/usr/bin/env python

# MT19937
# Mersenne Twister PRNG
class MTRNG:
    def __init__(self):
        self.m = 397 # middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
        self.n = 624 # degree of recurrence
        self.w = 32 # word size (bits)
        self.r = 31 # r: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w − 1
        self.f = 1812433253
        self.a = 0x9908B0DF # a: coefficients of the rational normal form twist matrix
        (self.s, self.b) = (7, 0x9D2C5680)  # TGFSR(R) Tempering bit shift + mask
        (self.t, self.c) = (15, 0xEFC60000) # TGFSR(R) Tempering bit shift + mask
        (self.u, self.d) = (11, 0xFFFFFFFF) # additional Mersenne Twister tempering bit shifts/masks
        self.l = 18 # additional Mersenne Twister tempering bit shifts/masks

        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (
            1 << self.r
        ) - 1  #  1111111111111111111111111111111 r=31 "the binary number of r 1's"
        self.upper_mask = (
            self.lower_mask + 1
        )  # 10000000000000000000000000000000 w=32 "lowest w bits of (not lower_mask)"

    def seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            x = self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i
            # Get the "lowest w bits" of the above number
            mask = (1 << self.w) - 1
            self.MT[i] = x & mask

    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                raise ValueError("Generator was never seeded")
            self.twist()
        y = self.MT[self.index]
        # print(f"before: {y} {y:32b} ")
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index += 1
        mask = (1 << self.w) - 1
        # print(f"after : {(y&mask)} {(y&mask):32b}")
        return y & mask

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[ (i+self.m) % self.n ] ^ xA
        self.index = 0
