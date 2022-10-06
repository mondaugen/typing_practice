import random
import defs
import rwalk
import numpy as np
import itertools
from common import get_env
import pickle

def create(
    charset,
    word_len=5,
    n_chars=3,
    n_words_per_line=10,
    n_lines=10,
    # probability of two different consecutive characters  
    change_prob=0.95,
    line_ending="*\n"):

    n_output_chars=n_words_per_line*n_lines*word_len
    chars=random.sample(charset,n_chars)
    chars=np.array([ord(c) for c in chars])
    ci=np.array(rwalk.weighted1(n_output_chars,n_chars,change_prob),dtype='int')
    chars=chars[ci]
    out_chars="".join([chr(c) for c in chars])

    n=0
    s=''
    for l in range(n_lines):
        for w in range(n_words_per_line):
            s+=out_chars[n:n+word_len]+' '
            n+=word_len
        s+=line_ending

    return s

class program:
    """
    A complete training program for a character set.
    Upon initialization, the character set is shuffled.
    Then when a problem set is requested, the next n_chars are taken from the
    character set. Then the pairs (a,b) s.t. {a,b in character sub set} are
    created and stored in a shuffled sequence. Words are synthesized by
    concatenating sucessive pairs. When all the pairs are exhausted, but words
    remain to be synthesized, the set is shuffled and the concatenation
    continues. This set of words is returned as the problem set. The position in
    the character sequence is stored so that the next request for a problem set gives
    new characters (unless the characters have been exhausted, in which case the
    pair sequence is shuffled and we start the whole thing again).
    """
    def new_program(self):
        random.shuffle(self.charset)
        self.charset_pos=0
        self.n_prog+=1
    def __init__(self,charset):
        assert(len(charset)>0)
        self.charset=list(charset)
        self.n_prog=-1
        self.new_program()
    def get_next_char(self):
        r=self.charset[self.charset_pos]
        self.charset_pos+=1
        if self.charset_pos >= len(self.charset):
            self.new_program()
        return r
    def problem_set(self,
                    word_len=5,
                    n_chars=3,
                    n_words_per_line=10,
                    n_lines=10,
                    line_ending="*\n"):
        n_output_chars=n_words_per_line*n_lines*word_len
        chars=[self.get_next_char() for _ in range(n_chars)]
        # remove identical pairs because we get enough repeats without them
        char_pairs=list(filter(lambda p : p[0] != p[1],itertools.product(chars,chars)))
        random.shuffle(char_pairs)
        cpi=iter(char_pairs)
        output_chars=''
        for n in range(0,n_output_chars+2,2):
            try:
                p=next(cpi)
            except StopIteration:
                random.shuffle(char_pairs)
                cpi=iter(char_pairs)
                p=next(cpi)
            output_chars+="".join(p)
        n=0
        s=''
        for l in range(n_lines):
            for w in range(n_words_per_line):
                s+=output_chars[n:n+word_len]+' '
                n+=word_len
            s+=line_ending
        return (s,chars)

def run_training_set(TS_PATH,chars):
    n_chars=get_env('N_CHARS',default=13,conv=int)

    try:
        fd=open(TS_PATH,'rb')
        prog=pickle.load(fd)
        fd.close()
    except FileNotFoundError:
        prog=program(chars)

    prog_num=prog.n_prog
    s,c=prog.problem_set(n_chars=n_chars)

    with open(TS_PATH,'wb') as fd:
        pickle.dump(prog,fd)

    print("Program number:",prog_num)
    print("Characters:","".join(c))
    print(s,end='')
