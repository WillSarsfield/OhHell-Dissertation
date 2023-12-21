import unittest
from Card import Card
from Deck import Deck

class TestCards(unittest.TestCase):
    
    def testContains(self):
        deck1 = Deck()
        card1 = Card(14, 0)
        self.assertEqual(deck1.contains(card1), True)

    def testRemoveCard(self):
        deck1 = Deck()
        card1 = Card(14, 0)
        deck1.removeCard(card1)
        self.assertEqual(deck1.contains(card1), False)

    def testMakeHand(self):
        deck1 = Deck()
        hand1 = deck1.makeHand(5)
        self.assertEqual(len(hand1) == 5, True)
        self.assertEqual(len(deck1.getCards()) == 47, True)

if __name__ == '__main__':
    unittest.main()