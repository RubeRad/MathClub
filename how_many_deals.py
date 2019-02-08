#! /usr/bin/env python3

import argparse
import set



parser = argparse.ArgumentParser("How many deals have sets in them?")
parser.add_argument('-n', default=100, type=int, help='Number of shuffles/deals to simulate')
parser.add_argument('-k', default=12,  type=int, help='Number of cards per deal')
parser.add_argument('-v', action='store_true', help="Verbose")
args = parser.parse_args()

print(args.n, args.k)

counts = [0]*100 # start out with more than enough 0s
for deali in range(args.n):
    cards = set.deck()
    deal = []
    for cardi in range(args.k):
        deal.append(cards.pop())

    ijks = set.find_sets(deal)
    if not ijks:
        counts[0] += 1
        if args.v:
            print('Deal has 0 sets\n')
        continue

    counts[len(ijks)] += 1

    if (args.v):
        print('Deal has '+str(len(ijks))+' sets:')
        for idx in ijks:
            deal[idx].describe()
        print('')


print(set.histogram(counts))
print("mean: ", set.mean(counts))
print("no sets:" + str(counts[0]/args.n*100) + '%')
