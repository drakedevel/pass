#!/usr/bin/env python
"""Dictionary-based password generator.

Usage: pass.py [options]

Options:
  -h --help               Show this help text
  -d --dictionary=<path>  Specify a non-default dictionary
  -n --length=N           Specify number of words to use [default: 4]
  -v --verbose            Print entropy estimate
  --complex               Bypass complexity requirements
  --truncate=SIZE         Truncate dictionary to specified size
  --uncontrolled          Generate a naively-random password from the list

The default mode ensures words are spread throughout the list, slightly
reducing absolute entropy but generally improving password memorability if the
dictionary is ordered by frequency.
"""
import math
import os
from docopt import docopt
from secrets import SystemRandom


def main():
    # Normalize arguments
    args = docopt(__doc__)
    word_count = int(args['--length'])

    # Read and transform dictionary file
    if args['--dictionary']:
        dict_path = args['--dictionary']
    else:
        dict_path = os.path.join(os.path.dirname(__file__), 'words.txt')
    dictionary = [w for w in [l.strip() for l in open(dict_path)] if w]
    if args['--truncate']:
        dictionary = dictionary[:int(args['--truncate'])]
    elif not args['--dictionary']:
        # Default truncation for built-in dictionary
        dictionary = dictionary[:8192]

    # Basic entropy calculation
    if args['--uncontrolled']:
        entropy = math.log(math.pow(len(dictionary), word_count), 2)
    else:
        batch_size = len(dictionary) // word_count
        entropy = math.log(math.pow(batch_size, word_count) *
                           math.factorial(word_count), 2)
    if args['--verbose']:
        print("Pessimistic password entropy: %.1f bits" % entropy)
        print("Approximate time to crack at 20k/s: %.1f days" %
              (math.pow(2, entropy) / 20000 / 60 / 60 / 24))

    # Generate password
    rng = SystemRandom()
    if args['--uncontrolled']:
        # Select random words
        words = [rng.choice(dictionary) for i in range(word_count)]
    else:
        # Generate batches in random order
        batches = [dictionary[i*batch_size:(i+1)*batch_size]
                   for i in range(word_count)]
        rng.shuffle(batches)

        # Select word from each batch
        words = [rng.choice(batches[i]) for i in range(word_count)]

    # Reveal to user
    print(" ".join(words))
    if args['--complex']:
        print("Complexified: %s1." % "".join(words).capitalize())


if __name__ == '__main__':
    main()
