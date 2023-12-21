from Card import Card
import random
import math

class Deck:
    def __init__(self) -> None:#builds deck of cards when initialised
        self.cardList = []
        values = list(range(2,15))
        suits = list(range(0,4))
        
        for suit in suits:
            for value in values:
                c = Card(value,suit)
                self.cardList.append(c)

    def __str__(self):
        string = ""
        for card in self.cardList:
            string += card.__str__()
            string += "  "
        return string
    
    def getCards(self):
        return self.cardList
    
    def shuffle(self):#shuffle deck function
        random.shuffle(self.cardList)
    
    def removeCard(self, card):
        newList = [c for c in self.cardList if not c.equalTo(card)]
        self.cardList = newList

    def makeHand(self, i):#deals hand of i cards from the top of the deck
        cards = self.cardList[:i]
        del self.cardList[:i]
        return cards
    
    def contains(self, card):
        for c in self.cardList:
            if card.equalTo(c):
                return True
        return False