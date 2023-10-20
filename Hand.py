import random

class Hand:
    def __init__(self, cardList) -> None:
        self.cardList = cardList
    
    def sort(self):
        sorted(self.cardList, key=lambda card: card.value)

    def shuffle(self):
        random.shuffle(self.cardList)

    def getCards(self):
        return self.cardList
    
    def pop(self):
        return self.cardList.pop(0)
    
    def __str__(self):
        string = ""
        for card in self.cardList:
            string += card.__str__()
            string += "  "
        return string