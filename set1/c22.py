#!/usr/bin/env python
from mt_rng import MTRNG
import random
import time

class RNGExercise:
    def delay_reseed_and_number(self):
        """
            - Wait a random number of seconds between, I don't know, 40 and 1000.
            - Seeds the RNG with the current Unix timestamp
            - Waits a random number of seconds again.
            - Returns the first 32 bit output of the RNG.
        """
        r = MTRNG()

        # Wait
        time.sleep(random.randint(40, 1000))

        # Seed RNG w/ Unix timestamp and save the seed
        self.seed = int( time.time() )
        r.seed_mt(self.seed)

        # Wait again
        time.sleep(random.randint(40, 1000))
        # time.sleep(random.randint(4, 10))

        # Return the first 32 bit output of the RNG
        return r.extract_number()

def main():
    re = RNGExercise()

    print("Getting random number..")
    timestamp_before = int( time.time() )
    output_num = re.delay_reseed_and_number()
    timestamp_after = int( time.time() )

    print(f"Function call: [{timestamp_before}] -> [{timestamp_after}]. Output: [{output_num}]")
    print("Scanning timestamp values for matches...")
    r = MTRNG()
    for guess_seed in range(timestamp_before, timestamp_after):
        r.seed_mt(guess_seed)
        guess_value = r.extract_number()
        if guess_value == output_num:
            print(f"Found match! Guessed seed=[{guess_seed}], Real Seed=[{re.seed}]")
            break
        elif guess_seed % 100 == 0:
            print(f"{guess_seed} didn't match.")



if __name__ == "__main__":
    main()
