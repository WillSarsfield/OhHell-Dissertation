import unittest
from Card import Card

class TestCards(unittest.TestCase):
    
    def testEqualTo(self):
        card1 = Card(3, 0)
        card2 = Card(3, 0)
        self.assertEqual(card1.equalTo(card2), True)
        card3 = Card(3, 1)
        self.assertEqual(card1.equalTo(card3), False)

    def testBeats(self):
        card1 = Card(3, 0)
        card2 = Card(5, 0)
        trump = 0
        leadSuit = 1
        self.assertEqual(card2.beats(card1, leadSuit, trump), True)
        card3 = Card(10, 1)
        self.assertEqual(card1.beats(card3, leadSuit, trump), True)
        card4 = Card(14, 1)
        self.assertEqual(card3.beats(card4, leadSuit, trump), False)
        card5 = Card(14, 0)
        self.assertEqual(card5.beats(card4, leadSuit, trump), True)

if __name__ == '__main__':
    unittest.main()