# Python 3.4 - sub-word search utility
# See accompanying LICENSE and README.md files for more info

import re
from collections import defaultdict
import sys

word_dict = defaultdict(set)

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

def find_word(word):
    global word_dict
    word = ''.join(sorted(list(word)))
    return word_dict[word]

def select(lst, n):
    if n == 0 or lst == [] or len(lst) < n:
        return [[]]
    elif n == 1:
        return [[e] for e in lst]
    elif len(lst) == n:
        return [lst]
    elif len(lst) > n:
        return [[lst[0]] + s for s in select(lst[1:], n-1)] + select(lst[1:], n)

def wselect(word, n):
    return {''.join(w) for w in select(list(word), n)}

def words(word_set):
    wset = set()
    for w in word_set:
        wl = find_word(w)
        if wl != set():
           wset = wset.union(wl)
    return wset

def get_words(wseq, n):
    return words(wselect(wseq, n))

class SessionRepl:
    def __init__(self):
        self.word = ''
        self.word_len = {}
        self.wset = False

    def set_word(self, w):
        self.word = w
        self.wset = True
        self.word_len = {}

    def print_words(self, n):
        if not self.wset:
            return
        s = set()
        if n not in self.word_len:
            s = get_words(self.word, int(n))
            self.word_len[n] = s
        else:
            s = self.word_len[n]
        print(s)

    def clear(self):
        self.word = ''
        self.word_len = {}
        self.wset = False

def help():
    m = '''
Available commands:
    :help: prints this message.
    <word>: sets the current word as <word>. All sub-words are taken from this one.
    :clear: removes current word. To set a new one, use set command.
    <length:int>: prints the set of sub-words of length <length> (an int) for the current word set. Shows nothing when no word is set.
    :quit: quits the REPL.
    '''
    print(m)
        
def repl():
    session = SessionRepl()
    session.clear()
    print('words-search utility\ntype :help to see available commands\ntype :quit to exit the prompt')
    while True:
        line = input('?- ').strip()
        parts = re.split(r'\s+', line)
        l = len(parts)
        if l < 0 or l > 2:
            print('*** Bad command')
            continue
        command = parts[0].upper()
        if command == ':HELP':
            help()
        elif command == ':CLEAR':
            session.clear()
        elif command == ':QUIT':
            sys.exit(0)
        elif re.match(r'[a-zA-Z]{1,}', command):
            word = parts[0].upper()
            session.set_word(word)
        elif re.match(r'\d+', command):
            length = int(command)
            session.print_words(length)
        else:
            print('*** Not sure what that means, try help')

if __name__ == '__main__':
    print('Loading dictionary... ', end='')
    sys.stdout.flush()
    load_words('words')
    print('done')
    repl()

    
