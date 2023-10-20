class Card:
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit

    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.value
    
    def __str__(self):
        suitDict = {
            0: "♥",
            1: "♦",
            2: "♠",
            3: "♣"
        }
        valueDict = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }
        if self.value in valueDict:
            return f"|{valueDict[self.value]} {suitDict[self.suit]}|"
        return f"|{self.value} {suitDict[self.suit]}|"
    