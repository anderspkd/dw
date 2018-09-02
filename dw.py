#!/usr/bin/env python3

import argparse
import re
import sys

pre = re.compile(r'^[1-6]{5}$')

p = argparse.ArgumentParser('diceware password generator')
p.add_argument('-l', metavar='length', dest='ln', help='password length (default 6)', type=int, default=6)
p.add_argument('-s', metavar='separator', dest='sep', help='separator (default " ")', default=' ')
p.add_argument('-u', dest='upper', help='uppercase password', action='store_true')
p.add_argument('-f', dest='fake_dice', action='store_true', help='emulate dice rolls')
p.add_argument('wordlist', help='wordlist to use', type=argparse.FileType('r'))

if len(sys.argv) == 1:
    p.print_help()
    exit(0)

args = p.parse_args()

if args.fake_dice:
    print(f'faking {5*args.ln} dicerolls')
else:
    print(f'gonna need {5*args.ln} dicerolls')

words = [w for w in args.wordlist]

def find_word(idx):
    b10 = 0
    i = 5
    for x in idx:
        i -= 1
        b10 += (6**i)*(int(x) - 1)
    return words[b10].rstrip()

pwd = list()

if args.fake_dice:

    from secrets import randbelow
    for i in range(args.ln):
        rolls = ''.join([str(1 + randbelow(6)) for _ in range(5)])
        pwd.append(find_word(rolls))

else:

    for i in range(args.ln):
        rolls = input('5 rolls, no spaces> ')
        assert pre.match(rolls), f'invalid roll={rolls}'
        pwd.append(find_word(rolls))

pwd = args.sep.join(pwd)
if args.upper:
    pwd = pwd.upper()
print(f'''
====== password ======
{pwd}
======================
''')
