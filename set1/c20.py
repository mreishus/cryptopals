#!/usr/bin/env python
import base64
from shared import ctr_crypt, random_aes_key, hex_bytes_xor
from eng_freq import frequency_score

def get_pts():
    return [
        'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
        'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
        'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
        'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
        'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
        'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
        'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
        'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
        'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
        'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
        'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
        'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
        'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
        'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
        'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
        'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
        'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
        'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
        'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
        'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
        'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
        'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
        'U2hlIHJvZGUgdG8gaGFycmllcnM/',
        'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
        'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
        'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
        'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
        'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
        'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
        'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
        'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
        'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
        'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
        'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
        'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
        'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
        'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
        'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
        'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
        'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
    ];

def main():
    print("c19")
    key = random_aes_key()
    print(key)
    print(key[0])
    pts = get_pts()

    # Encrypt all PTs with CTR using a fixed nonce
    fixed_nonce=b"\x00" * 8
    cts = []
    for pt in pts:
        pt = base64.b64decode(pt)
        ct = ctr_crypt(pt, key, fixed_nonce)
        cts.append(ct)
    # print(cts)

    key_guesses = []
    key_guess_string = bytearray()
    for i in range(200):
        guess_strings = {}
        guess_scores = {}
        for guess in range(0xff):
            guess_strings[guess] = bytearray()
            for ct in cts:
                if i >= len(ct):
                    continue
                decrypted = ct[i] ^ guess
                decrypted = decrypted.to_bytes(length = 1, byteorder='little')
                # print(f"ct[i] = {ct[i]}, guess = {guess}")
                guess_strings[guess] += bytes(decrypted)

            if len(guess_strings[guess]) == 0:
                continue

            decode_string = str("".join([chr(byte) for byte in guess_strings[guess]]))
            guess_scores[guess] = frequency_score(decode_string)

        if len(guess_scores) == 0:
            continue

        winner = min(range(0xff), key=lambda x: guess_scores[x])
        # print(f"winner: {winner}")
        key_guesses.append(winner)
        key_guess_string += winner.to_bytes(length = 1, byteorder='little')

    #print(key_guesses)
    #print(key_guess_string)

    for ct in cts:
        print(ct)
    # We have guessed the keystream and put it in key_guess_string
    for ct in cts:
        tmp_key = key_guess_string
        if len(tmp_key) > len(ct):
            tmp_key = tmp_key[:len(ct)]
        pt = hex_bytes_xor(ct, tmp_key)
        print(pt)

    # x = base64.b64decode(ct)
    # print(x)

if __name__ == "__main__":
    main()
