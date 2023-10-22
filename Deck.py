from Card import Card
import random

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
    
    def shuffle(self):
        random.shuffle(self.cardList)

    def makeHand(self):
        cards = self.cardList[:13]
        del self.cardList[:13]
        return cards