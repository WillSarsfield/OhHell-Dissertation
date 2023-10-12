import Card

class Deck:
    def __init__(self) -> None:
        self.cardList = []
        values = list(range(2,15))
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        
        for suit in suits:
            for value in values:
                self.cardList.append(c = Card(value,suit))

    def __str__(self):
        deckStr = []
        for card in self.cardList:
            deckStr.append(print(card))

        return deckStr