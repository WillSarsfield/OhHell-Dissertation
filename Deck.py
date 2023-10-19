from Card import Card
import random

class Deck:
    def __init__(self) -> None:
        self.cardList = []
        values = list(range(2,15))
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        
        for suit in suits:
            for value in values:
                c = Card(value,suit)
                self.cardList.append(c)

    def __str__(self):
        deckStr = []
        for card in self.cardList:
            deckStr.append(print(card))

        return deckStr
    
    def getCards(self):
        return self.cardList
    
    def shuffle(self):
        random.shuffle(self.cardList)

    def pop(self):
        return self.cardList.pop(0)