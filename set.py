#! /usr/bin/python3

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
def find_sets(cards):
    n = len(cards)
    sets = [];
    for i in range(0,n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                if (is_a_set(cards[i], cards[j], cards[k])):
                    sets.append( (i,j,k) )
    if len(sets):
        return sets
    # else
    return None

def has_a_set(cards):
    sets = find_sets(cards)
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

        def testHistogram(s):
            counts = [0]*82
            for i in range(100):
                cards = deck()
                deal = []
                while not has_a_set(deal):
                    deal.append(cards.pop())
                verbose = False
                if verbose:
                    ijks = find_sets(deal)
                    print(len(deal),"cards dealt, set(s) found:",len(ijks))
                    for ijk in ijks:
                        print("Set found:")
                        deal[ijk[0]].describe()
                        deal[ijk[1]].describe()
                        deal[ijk[2]].describe()
                counts[len(deal)] += 1

            while counts[-1]==0: counts.pop()
            for i in range(3,len(counts)):
                print(str(i)+":", counts[i])


    unittest.main()



