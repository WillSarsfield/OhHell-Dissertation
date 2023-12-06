class Card:#basic class defining individual cards through integers
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit

    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.value

    def equalTo(self, card):
        if self.value == card.value and self.suit == card.suit:
            return True
        return False
    
    def __str__(self):#print card translates integers used for suits and values to correct symbols
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
            return f"|{valueDict[self.value]:<2} {suitDict[self.suit]}|"
        return f"|{self.value:<2} {suitDict[self.suit]}|"
    