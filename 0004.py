#! /usr/bin/python3

import sys
import re

def count_word(file):
    word_count = {}
    with open(file) as f:
        for line in f:
            words = re.split(r'[ \,\.\?\!\;\"\'\[\]\{\}\<\>\(\)]', line)
            for word in words:
                if word in word_count.keys():
                    word_count[word] = word_count[word] + 1
                else:
                    word_count[word] = 1

    return word_count

if __name__ == '__main__':
    word_count = count_word(sys.argv[1])
    for k, v in word_count:
        print("%s : %d", k, v)
