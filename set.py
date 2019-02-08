#! /usr/bin/env python3

from random import randrange

nnicks={'1':1, '2':2, '3':3}
tnicks={'s':'solid', 't':'striped', 'o':'open'}
cnicks={'r':'red',   'g':'green',   'p':'purple'}
snicks={'r':'rect',  'o':'oval',    's':'squiggle'}

# three is the list of all three possibilities
# one and two are the two characteristics we have
# function returns that the third should be
def third(three, one, two):
    if one==two:
        return one # two the same-->third must be the same
    #else one and two are different, return the other one
    for other in three:
        if other != one and other != two:
            return other

class SetCard():
    def __init__(s, code):
        s.code = code
        if not s.valid():
            raise ValueError('Invalid code: '+code)

    def __eq__(one, two):
        return isinstance(two, SetCard) and one.code==two.code

    def __ne__(one, two):
        return not one.__eq__(two)

    def number (s): return    int(s.code[0])
    def texture(s): return tnicks[s.code[1]]
    def color  (s): return cnicks[s.code[2]]
    def shape  (s): return snicks[s.code[3]]

    def valid(s):
        if not s.code or len(s.code)!=4: return False
        if s.number()<1 or s.number()>3: return False
        return s.code[1] in tnicks and s.code[2] in cnicks and s.code[3] in snicks

    def describe(s):
        if s.number()==1:
            print(s.number(), s.texture(), s.color(), s.shape())
        else:
            print(s.number(), s.texture(), s.color(), s.shape()+'s')

    # given this card and a 2nd, return the third that would make a set
    def third(one, two):
        code = (str(third(nnicks.keys(), one.code[0], two.code[0])) +
                    third(tnicks.keys(), one.code[1], two.code[1]) +
                    third(cnicks.keys(), one.code[2], two.code[2])   +
                    third(snicks.keys(), one.code[3], two.code[3]))
        return SetCard(code)


def is_a_set(one, two, three):
    need = one.third(two)
    return three == one.third(two)

# returns 3-tuples the _indices_ of any sets among these cards
def find_sets(cards, force_last=False, quit_after_one=False):
    n = len(cards)
    sets = [];
    for i in range(0,n):
        for j in range(i+1,n):
            kmin = j+1
            kmax = n
            if force_last:
                kmin = n-1 
            for k in range(kmin, kmax):
                if (is_a_set(cards[i], cards[j], cards[k])):
                    sets.append( (i,j,k) )
                    if quit_after_one:
                        return sets

    if len(sets):
        return sets
    # else
    return None

def has_a_set(cards, must_include_last=False):
    sets = find_sets(cards, force_last=must_include_last, quit_after_one=True)
    if sets: return True
    # else
    return False

def deck(shuffle=True):
    cards = []
    for    n in nnicks.keys():
     for   t in tnicks.keys():
      for  c in cnicks.keys():
       for s in snicks.keys():
        cards.append(SetCard(n+t+c+s))

    if shuffle:
        n = len(cards)
        for i in range(n):    # swap every card
            j = randrange(n)  # with a random card
            cards[i],cards[j] = cards[j],cards[i]

    return cards

def histogram(counts, maxchars=70):
    histr = ''

    firsti = 0
    while firsti<len(counts) and counts[firsti]==0:
        firsti += 1
    # now firsti is the index of the first nonzero

    lasti = len(counts)-1  # avoid empties at the end
    while lasti>=0 and counts[lasti]==0:
        lasti -= 1
    # now lasti is the index of the last nonzero
    lasti += 1 # bump back up one

    maxcount = counts[firsti]
    for c in counts:
        if c > maxcount:
            maxcount = c

    scale = 1.0
    if maxcount > maxchars:
        scale = maxchars/maxcount


    for i in range(firsti, lasti):
        if i<10:
            histr += ' '
        nchar = round(counts[i] * scale)
        histr += str(i) + ': ' + '#' * nchar + ' ' + str(counts[i]) + '\n'

    return histr

def mean(counts):
    sum = 0
    num = 0
    for i in range(len(counts)):
        num += counts[i]
        sum += counts[i]*i
    if num==0:
        return None
    return sum/num



#######################
##### UNIT TESTS ######
#######################
import unittest
if __name__ == '__main__':
    class SetCardTester(unittest.TestCase):
        def testSetCards(s):
            exception=False
            try:     osrr = SetCard('1srr')
            except:  exception=True
            s.assertFalse(exception)
            s.assertEqual(osrr.number(),   1)
            s.assertEqual(osrr.texture(), 'solid')
            s.assertEqual(osrr.color(),   'red')
            s.assertEqual(osrr.shape(),   'rect')

            exception=False
            try:     ttgo = SetCard('2tgo')
            except:  exception=True
            s.assertFalse(exception)
            s.assertEqual(ttgo.number(),   2)
            s.assertEqual(ttgo.texture(), 'striped')
            s.assertEqual(ttgo.color(),   'green')
            s.assertEqual(ttgo.shape(),   'oval')

            exception = False
            try:      tops = SetCard('3ops')
            except:   exception = True
            s.assertFalse(exception)
            s.assertEqual(tops.number(), 3)
            s.assertEqual(tops.texture(), 'open')
            s.assertEqual(tops.color(), 'purple')
            s.assertEqual(tops.shape(), 'squiggle')

            s.assertEqual(osrr.third(ttgo), tops)
            s.assertEqual(ttgo.third(osrr), tops)
            s.assertEqual(tops.third(ttgo), osrr)

            s.assertTrue( is_a_set(  osrr, ttgo, tops))
            s.assertTrue(has_a_set( [osrr, ttgo, tops] ))

            cards = deck()
            s.assertEqual(len(cards), 3*3*3*3) # 81

        def testShortcuts(s):
            for i in range(100):
                cards = deck()
                deal = []
                no_sets = True # with an empty deal!
                while no_sets:
                    deal.append(cards.pop())
                    all_sets    = find_sets(deal) # full search, trusted result
                    sets_w_last = find_sets(deal, force_last=True)
                    if all_sets:
                        stophere=1
                    sets_max_1  = find_sets(deal, quit_after_one=True)
                    sets_last_1 = find_sets(deal, force_last=True, quit_after_one=True)
                    if all_sets: # not None
                        s.assertEqual(sets_w_last, all_sets)
                        s.assertEqual(len(sets_max_1), 1)
                        s.assertEqual(len(sets_last_1), 1)
                        s.assertEqual(sets_max_1, sets_last_1)
                        s.assertEqual(sets_max_1[0], sets_w_last[0])
                        no_sets = False # go shuffle a new deal
                    else: # all_sets is None
                        s.assertIsNone(sets_w_last)
                        s.assertIsNone(sets_max_1)
                        s.assertIsNone(sets_last_1)


    unittest.main()



