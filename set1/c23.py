#!/usr/bin/env python
from mt_rng import MTRNG
import random
import time

def main():
    r = MTRNG()
    print('hi')
    r.seed_mt(100)
    print(r.extract_number())


if __name__ == "__main__":
    main()
