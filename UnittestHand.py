import unittest
from Hand import Hand
from Card import Card

class TestHand(unittest.TestCase):
    
    def testRemove(self):
        card1 = Card(3, 0)
        card2 = Card(5, 0)
        card3 = Card(9, 1)
        cardList = []
        cardList.append(card1)
        cardList.append(card2)
        cardList.append(card3)
        hand1 = Hand(cardList)
        cardList.remove(card1)
        hand1.remove(card1)
        self.assertEqual(hand1.cardList == cardList, True)

    def testSort(self):
        card1 = Card(9, 1)
        card2 = Card(5, 0)
        card3 = Card(3, 0)     
        cardList = []
        cardList.append(card1)
        cardList.append(card2)
        cardList.append(card3)
        hand1 = Hand(cardList)
        hand1.sort()
        cardList = []
        cardList.append(card3)
        cardList.append(card2)
        cardList.append(card1)
        for i, card in enumerate(cardList):
            self.assertEqual(hand1.cardList[i].equalTo(card), True)

if __name__ == '__main__':
    unittest.main()