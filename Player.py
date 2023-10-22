import RandomAI

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []
        self.score = 0
        self.roundScore = 0
        self.bid = 0
    
    def getName(self):
        return self.name
    
    def getHand(self):
        return self.hand
    
    def makeHand(self, hand):
        self.hand = hand

    def sortHand(self):
        self.hand.sort()
    
    def shuffleHand(self):
        self.hand.shuffle()

    def getScore(self):
        return self.score
    
    def getRoundScore(self):
        return self.roundScore
    
    def getBid(self):
        return self.bid
    
    def addScore(self, x):
        self.score += x
        self.roundScore = 0

    def addRoundScore(self, x):
        self.roundScore += x
    
    def makeBid(self, bid):
        self.bid = bid

    def getOptions(self, lead = -1):#get card list of options to play given the lead suit
        if lead == -1:
            return self.hand.getCards()
        options = []
        for card in self.hand.getCards():
            if card.getSuit() == lead:
                options.append(card)
        if not options:
            options = self.hand.getCards()
        return options
    
    def playRandomOption(self, options):
        card = RandomAI.chooseCard(options)
        self.hand.remove(card)
        return card
    
    def playRandomBid(self, ban):
        self.bid = RandomAI.chooseBid(ban)

    def __str__(self):
        string = self.name + ": "
        string += self.hand.__str__()
        return string