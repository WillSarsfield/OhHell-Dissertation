import random
import math
from Card import Card

class Hand:#class that stores a players hand
    def __init__(self, cardList) -> None:
        self.cardList = cardList
    
    def sort(self): #sorts hand by changing the values mathematically, sorted the list of ints, and translating them back to cards
        valList = []
        newList = []
        for card in self.cardList:
            valList.append(card.getValue() - 2 + (card.getSuit() * 14))
        valList = sorted(valList)
        for val in valList:
            card = Card((val % 14) + 2, math.floor(val / 14))
            newList.append(card)
        self.cardList = newList

    def shuffle(self):#players can shuffle hand if they wish
        random.shuffle(self.cardList)

    def getCards(self):
        return self.cardList
    
    def pop(self):
        return self.cardList.pop(0)
    
    def remove(self, card):
        for c in self.cardList:
            if c.getValue() == card.getValue() and c.getSuit() == card.getSuit():
                self.cardList.remove(c)
    
    def __str__(self):
        string = ""
        for card in self.cardList:
            string += card.__str__()
            string += "  "
        return string