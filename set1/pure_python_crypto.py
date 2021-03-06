#!/usr/bin/env python

# All of this is from https://www.acooke.org/cute/PurePython0.html

"""

I am working through the Matasano Crypto Challenges -
http://www.matasano.com/articles/crypto-challenges/ - which I would recommend
to anyone interested in crypto.

Although they repeatedly ask not to post solutions online, they do ask (in
part 4, I think) for you to find (rather than implement) implementations of
SHA1 and MD4.  So I hope that it is OK for me to post these.

The two implementations are based on code at
https://raw.github.com/ajalt/python-sha1/master/sha1.py and
http://www.oocities.org/rozmanov/python/md4.html - the latter of those is
licensed under the LGPL and so the derivative work below is licensed the same
way.

While I am grateful to the two authors above (AJ Alt and Dmitry Rozmanov) I
have *extensively* reworked the code.  I hope that the implementation below
helps show the common structure shared by both.  And if you thought "MD
padding" meant "Message Digest padding" then you should read
http://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction

Also, note that I use generators whenever possible, so you may need to wrap
things in bytes(...) to get a byte array.


First, a few library routines:
"""

from itertools import zip_longest


def grouped(iterable, n, fillvalue=None):
    """group in to chunks - http://stackoverflow.com/a/434411/181772"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def little_endian_bytes(words, n):
    """convert n-byte words to bytes (little endian)"""
    for word in words:
        for _ in range(n):
            yield word & 0xFF
            word >>= 8


def big_endian_bytes(words, n):
    """convert n-byte words to bytes (big endian)"""
    for word in words:
        yield from reversed(list(little_endian_bytes([word], n)))


def big_endian_words(b, n):
    """convert bytes into n-byte words (big endian)"""
    for g in grouped(b, n):
        w = 0
        for b in g:
            w = w << 8 | b
        yield w


def little_endian_words(b, n):
    """convert bytes into n-byte words (little endian)"""
    for g in grouped(b, n):
        yield from big_endian_words(reversed(g), n)


"""
Now the crypto:
"""

import struct

# from cpals.common.bit import big_endian_bytes, little_endian_bytes, little_endian_words


# https://raw.github.com/ajalt/python-sha1/master/sha1.py
# (modified)

# http://www.oocities.org/rozmanov/python/md4.html
# Copyright (C) 2001-2002  Dmitry Rozmanov (LGPL)
# modified


def left_rotate(n, b):
    return ((n << b) | ((n & 0xFFFFFFFF) >> (32 - b))) & 0xFFFFFFFF


def md_pad_64(message, length_to_bytes, fake_byte_len=None):
    original_byte_len = len(message)
    message += b"\x80"
    message += b"\x00" * ((56 - (original_byte_len + 1) % 64) % 64)
    original_bit_len = (fake_byte_len if fake_byte_len else original_byte_len) * 8

    # debug = {
    #     'original_byte_len': original_byte_len,
    #     'times_8': original_byte_len * 8,
    #     'fake_byte_len': fake_byte_len,
    #     'bit_len': original_bit_len,
    # }
    # print(debug)

    message += bytes(length_to_bytes(original_bit_len))
    return message


def make_md_hash_64(compress, state_to_hash, length_to_bytes):
    def md_hash(message, fake_byte_len=None, state=None):
        message = md_pad_64(message, length_to_bytes, fake_byte_len=fake_byte_len)
        for i in range(0, len(message), 64):
            state = compress(message[i : i + 64], state)
        # print({
        #     'state': state,
        #     'state_to_hash': bytes(state_to_hash(state)).hex(),
        # })
        return state_to_hash(state)

    return md_hash


def sha1_compress(block, state=None):

    if not state:
        state = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    a, b, c, d, e = h0, h1, h2, h3, h4 = state

    w = [0] * 80
    # break chunk into sixteen 32-bit big-endian words w[i]
    for j in range(16):
        w[j] = struct.unpack(">I", block[j * 4 : j * 4 + 4])[0]
    # extend the sixteen 32-bit words into eighty 32-bit words:
    for j in range(16, 80):
        w[j] = left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

    for i in range(80):
        if i < 20:
            f = d ^ (
                b & (c ^ d)
            )  # use alternative 1 for f from FIPS PB 180-1 to avoid ~
            k = 0x5A827999
        elif 20 <= i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif 60 <= i:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        a, b, c, d, e = (
            (left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF,
            a,
            left_rotate(b, 30),
            c,
            d,
        )

    return [
        (h0 + a) & 0xFFFFFFFF,
        (h1 + b) & 0xFFFFFFFF,
        (h2 + c) & 0xFFFFFFFF,
        (h3 + d) & 0xFFFFFFFF,
        (h4 + e) & 0xFFFFFFFF,
    ]


SHA1 = make_md_hash_64(
    sha1_compress,
    lambda state: big_endian_bytes(state, 4),
    lambda length: big_endian_bytes([length], 8),
)


def f(x, y, z):
    return x & y | ~x & z


def g(x, y, z):
    return x & y | x & z | y & z


def h(x, y, z):
    return x ^ y ^ z


def f1(a, b, c, d, k, s, X):
    return left_rotate(a + f(b, c, d) + X[k], s)


def f2(a, b, c, d, k, s, X):
    return left_rotate(a + g(b, c, d) + X[k] + 0x5A827999, s)


def f3(a, b, c, d, k, s, X):
    return left_rotate(a + h(b, c, d) + X[k] + 0x6ED9EBA1, s)


def md4_compress(block, state=None):

    if not state:
        state = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
    a, b, c, d = h0, h1, h2, h3 = state

    x = list(little_endian_words(block, 4))

    a = f1(a, b, c, d, 0, 3, x)
    d = f1(d, a, b, c, 1, 7, x)
    c = f1(c, d, a, b, 2, 11, x)
    b = f1(b, c, d, a, 3, 19, x)
    a = f1(a, b, c, d, 4, 3, x)
    d = f1(d, a, b, c, 5, 7, x)
    c = f1(c, d, a, b, 6, 11, x)
    b = f1(b, c, d, a, 7, 19, x)
    a = f1(a, b, c, d, 8, 3, x)
    d = f1(d, a, b, c, 9, 7, x)
    c = f1(c, d, a, b, 10, 11, x)
    b = f1(b, c, d, a, 11, 19, x)
    a = f1(a, b, c, d, 12, 3, x)
    d = f1(d, a, b, c, 13, 7, x)
    c = f1(c, d, a, b, 14, 11, x)
    b = f1(b, c, d, a, 15, 19, x)

    a = f2(a, b, c, d, 0, 3, x)
    d = f2(d, a, b, c, 4, 5, x)
    c = f2(c, d, a, b, 8, 9, x)
    b = f2(b, c, d, a, 12, 13, x)
    a = f2(a, b, c, d, 1, 3, x)
    d = f2(d, a, b, c, 5, 5, x)
    c = f2(c, d, a, b, 9, 9, x)
    b = f2(b, c, d, a, 13, 13, x)
    a = f2(a, b, c, d, 2, 3, x)
    d = f2(d, a, b, c, 6, 5, x)
    c = f2(c, d, a, b, 10, 9, x)
    b = f2(b, c, d, a, 14, 13, x)
    a = f2(a, b, c, d, 3, 3, x)
    d = f2(d, a, b, c, 7, 5, x)
    c = f2(c, d, a, b, 11, 9, x)
    b = f2(b, c, d, a, 15, 13, x)

    a = f3(a, b, c, d, 0, 3, x)
    d = f3(d, a, b, c, 8, 9, x)
    c = f3(c, d, a, b, 4, 11, x)
    b = f3(b, c, d, a, 12, 15, x)
    a = f3(a, b, c, d, 2, 3, x)
    d = f3(d, a, b, c, 10, 9, x)
    c = f3(c, d, a, b, 6, 11, x)
    b = f3(b, c, d, a, 14, 15, x)
    a = f3(a, b, c, d, 1, 3, x)
    d = f3(d, a, b, c, 9, 9, x)
    c = f3(c, d, a, b, 5, 11, x)
    b = f3(b, c, d, a, 13, 15, x)
    a = f3(a, b, c, d, 3, 3, x)
    d = f3(d, a, b, c, 11, 9, x)
    c = f3(c, d, a, b, 7, 11, x)
    b = f3(b, c, d, a, 15, 15, x)

    return [
        (h0 + a) & 0xFFFFFFFF,
        (h1 + b) & 0xFFFFFFFF,
        (h2 + c) & 0xFFFFFFFF,
        (h3 + d) & 0xFFFFFFFF,
    ]


MD4 = make_md_hash_64(
    md4_compress,
    lambda state: little_endian_bytes(state, 4),
    lambda length: little_endian_bytes([length], 8),
)
