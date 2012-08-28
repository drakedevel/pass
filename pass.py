#!/usr/bin/env python
import Crypto.Random.random as random
import math
import sys

def main(wordlist, word_count, candidate_count = 8192, mode = "controlled", quiet = None):
    # Normalize inputs
    word_count = int(word_count)
    candidate_count = int(candidate_count)
    if mode not in ('controlled', 'random'):
        raise Exception("Unknown mode '%s'" % mode)

    # Basic entropy calculation
    if mode == 'controlled':
        batch_size = candidate_count // word_count
        entropy = math.log(math.pow(batch_size, word_count) * math.factorial(word_count)) / math.log(2)
    else:
        entropy = math.log(math.pow(candidate_count, word_count)) / math.log(2)
    if quiet != "quiet":
        print "Pessimistic password entropy: %.1f bits" % entropy
        print "Approximate time to crack at 20k/s: %.1f days" % (math.pow(2, entropy) / 20000 / 60 / 60 / 24)

    # Read in candidate words
    with open(wordlist, 'r') as wordlist_file:
        candidates = [s.strip() for s in wordlist_file.readlines()[0:candidate_count]]

    # Generate password
    if mode == 'controlled':
        # Generate batches in random order
        batches = [candidates[i*batch_size:(i+1)*batch_size] for i in range(word_count)]
        random.shuffle(batches)

        # Select word from each batch
        words = [random.choice(batches[i]) for i in range(word_count)]
    else:
        # Select random words
        words = [random.choice(candidates) for i in range(word_count)]

    # Reveal to user
    print " ".join(words)

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print "Usage: pass.py <wordlist> <word count> [<candiate words> [<mode> [quiet]]]"
        sys.exit(1)
    main(*sys.argv[1:])
