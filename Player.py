class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []
        self.score = 0
        self.bid = 0
    
    def getName(self):
        return self.name
    
    def getHand(self):
        return self.hand
    
    def makeHand(self, hand):
        self.hand = hand

    def getScore(self):
        return self.score
    
    def getBid(self):
        return self.bid
    
    def addScore(self, x):
        self.score += x
    
    def makeBid(self, bid):
        self.bid = bid

    def __str__(self):
        string = self.name + ": "
        string += self.hand.__str__()
        return string