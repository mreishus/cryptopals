#!/usr/bin/env python

from collections import Counter
import math

# Estimated value of letter frequency in English
eng_freq = {
    "a": .084966,
    "b": .020720,
    "c": .045388,
    "d": .033844,
    "e": .111607,
    "f": .018121,
    "g": .024705,
    "h": .030034,
    "i": .075448,
    "j": .001965,
    "k": .011016,
    "l": .054893,
    "m": .030129,
    "n": .066544,
    "o": .071635,
    "p": .031671,
    "q": .001962,
    "r": .075809,
    "s": .057351,
    "t": .069509,
    "u": .036308,
    "v": .010074,
    "w": .012899,
    "x": .002902,
    "y": .017779,
    "z": .002722,
}


def compute_eng_freq_with_spaces(eng_freq):
    """
    Given an english character frequency list without space, add a space
    character and scale down the rest of the frequencies accordingly, so the
    sum is still 100%.
    """
    space_freq_estimate = 0.15
    output = {
        ' ': space_freq_estimate,
    }
    for letter, letter_freq in eng_freq.items():
        output[letter] = letter_freq  * (1.0 - space_freq_estimate)
    return output

eng_freq_with_spaces = compute_eng_freq_with_spaces(eng_freq)

def frequency_score(str_in):
    str_in = str_in.lower()
    counts = Counter(str_in)

    if len(str_in) == 0:
        return 0

    total_diff = 0.0
    sum_diff = 0.0
    for letter, ideal_freq in eng_freq_with_spaces.items():
        actual_freq = counts[letter] / len(str_in)
        this_diff = ideal_freq - actual_freq
        total_diff += this_diff * this_diff
        sum_diff += this_diff
        # print(f"let={letter} idea={ideal_freq} act={actual_freq} diff={this_diff} total={total_diff}")

    return sum_diff
    return math.sqrt(total_diff)

