# A generator version of words lookup
# Still early for use in a concurrent setup

import re
from collections import defaultdict
import sys

word_dict = defaultdict(set)


def select(lst, n):
    if n <= 0 or len(lst) == 0 or len(lst) < n:
        yield [[]]
    elif n == 1:
        for e in [[x] for x in lst]:
            yield e
    else:
        sub_g1 = select(lst[1:], n - 1)
        sub_g2 = select(lst[1:], n)
        for x in sub_g1:
            if x != [[]]:
                yield [lst[0]] + x
            else:
                yield [lst[0]]
        for y in sub_g2:
            if y != [[]]:
                yield y

        
def sorted_key_select(word, n):
    lst = [x.upper() for x in sorted(list(word))]
    gen = select(lst, n)
    for l in gen:
        e = ''.join(l)
        yield e

def lookup_word(word, n):
    global word_dict
    gen = sorted_key_select(word, n)
    for w in gen:
        if w in word_dict:
            yield word_dict[w]

def load_words(file):
    global word_dict
    f = open(file)
    for line in f:
        line = line.strip()
        match = re.match(r'(\w+)', line)
        if match:
            wv = match.group(1).upper()
            wk = ''.join(sorted(list(wv)))
            word_dict[wk].add(wv)
    f.close()

