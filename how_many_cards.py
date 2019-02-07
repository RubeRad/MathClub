#! /usr/bin/env python3

import argparse
import set



parser = argparse.ArgumentParser("How many cards need to be dealt until there's a set?")
parser.add_argument('-n', default=100, type=int, help='Number of shuffles/deals to simulate')
parser.add_argument('-v', action='store_true', help="Verbose")
args = parser.parse_args()

print(args.n)

counts = [0]*82       # 0 not used, 1-81 might(?) get populated
for i in range(args.n):
    cards = set.deck()
    deal = []
    while not set.has_a_set(deal):
        deal.append(cards.pop())

    if args.v:
        ijks = set.find_sets(deal)
        print(len(deal),"cards dealt, set(s) found:",len(ijks))
        for ijk in ijks:
            print("Set found:")
            deal[ijk[0]].describe()
            deal[ijk[1]].describe()
            deal[ijk[2]].describe()
    counts[len(deal)] += 1

print(set.histogram(counts))
