#! /usr/bin/env python3

import argparse
import set



parser = argparse.ArgumentParser("How many cards need to be dealt until there's a set?")
parser.add_argument('-n', default=100, type=int, help='Number of shuffles/deals to simulate')
parser.add_argument('-v', action='store_true', help="Verbose")
parser.add_argument('-i', default=10000, type=int, help='Interval for printing intermediate histograms')
parser.add_argument('-o', default=None, type=str, help='File to write all counts to')
args = parser.parse_args()

file = None
if args.o:
    file = open(args.o, mode="w")

print(args.n)

counts = [0]*82       # 0 not used, 1-81 might(?) get populated
for i in range(args.n):
    cards = set.deck()
    deal = []
    while set.find_sets(deal, force_last=True, quit_after_one=True) is None:
        deal.append(cards.pop())

    counts[len(deal)] += 1
    if  file:
        file.write(str(len(deal))+'\n')

    if args.v:
        ijks = set.find_sets(deal)
        print(len(deal),"cards dealt, set(s) found:",len(ijks))
        for ijk in ijks:
            print("Set found:")
            deal[ijk[0]].describe()
            deal[ijk[1]].describe()
            deal[ijk[2]].describe()

    if i>0 and i%args.i == 0:
        print("Simulations: ", i)
        print(set.histogram(counts))

print(set.histogram(counts))
