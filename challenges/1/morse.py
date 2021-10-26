#!/usr/bin/env python3

import sys

def morse(text):
    char_map = {
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        'd': '-..',
        'e': '.',
        'f': '..-.',
        'g': '--.',
        'h': '....',
        'i': '..',
        'j': '.---',
        'k': '-.-',
        'l': '.-..',
        'm': '--',
        'n': '-.',
        'o': '---',
        'p': '.--.',
        'q': '--.-',
        'r': '.-.',
        's': '...',
        't': '-',
        'u': '..--',
        'v': '...-',
        'w': '.--',
        'x': '-..-',
        'y': '-.--',
        'z': '--..',
        ' ': '|',
    }
    result = []
    for letter in text.lower():
        if letter not in char_map:
            continue
        for c in char_map[letter]:
            result.append(c)
        result.append(' ')
    return ''.join(result[:-1])

def morse_signal(text):
    morse_text = morse(text)
    signal_map = {
        '.': '. ',
        '-': '... ',
        ' ': '  ',
        '|': '      ',
    }
    result = []
    for letter in morse_text:
        result.append(signal_map[letter])
    return ''.join(result)

if __name__ == '__main__':
    text = sys.argv[1]
    print(morse(text))
    print(morse_signal(text))
