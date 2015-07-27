# A generator version of words lookup
# Still early for use in a concurrent setup

from collections import defaultdict

class Words:
    def __init__(self, wordfile='words'):
        self.wordfile = wordfile
        self.word_dict = defaultdict(set)
        self.load_words()

    def load_words(self):
        f = open(self.wordfile)
        for line in f:
            line = line.strip()
            match = re.match(r'(\w+)', line)
            if match:
                wv = match.group(1).upper()
                wk = ''.join(sorted(list(wv)))
                self.word_dict[wk].add(wv)
        f.close()

    def select(self, lst, n):
        if n <= 0 or len(lst) == 0 or len(lst) < n:
            yield [[]]
        elif n == 1:
            for e in [[x] for x in lst]:
                yield e
        else:
            sub_g1 = self.select(lst[1:], n - 1)
            sub_g2 = self.select(lst[1:], n)
            for x in sub_g1:
                if x != [[]]:
                    yield [lst[0]] + x
                else:
                    yield [lst[0]]
            for y in sub_g2:
                if y != [[]]:
                    yield y
                                
    def sorted_key_select(self, word, n):
        lst = [x.upper() for x in sorted(list(word))]
        gen = self.select(lst, n)
        for l in gen:
            e = ''.join(l)
            yield e

    def lookup_word(self, word, n):
        gen = self.sorted_key_select(word, n)
        for w in gen:
            if w in word_dict:
                yield self.word_dict[w]

