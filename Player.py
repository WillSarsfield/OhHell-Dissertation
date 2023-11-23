import random

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []
        self.score = 0 #cumulative score
        self.roundScore = 0 #score over a single round
        self.bid = 0 #bid for current round
        self.handHistory = []
        self.scoreHistory = []
    
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

    def addHandHistory(self, cards):
        self.handHistory.append(cards)
    
    def getHandHistory(self):
        return self.handHistory
    
    def addScoreHistory(self, score):
        self.scoreHistory.append(score)

    def getScoreHistory(self):
        return self.scoreHistory

    def getOptions(self, lead = -1):#get card list of options to play given the lead suit
        if lead == -1: #if nothing passed into function, no suit has been played so any card is an option
            return self.hand.getCards()
        options = []
        for card in self.hand.getCards(): #add cards of the same suit as the lead to the options
            if card.getSuit() == lead:
                options.append(card)
        if not options: #if no cards with the same suit as the lead, all cards are options
            options = self.hand.getCards()
        return options
    
    def playOption(self, options, cardsPlayed, trump): #picks a random card out of the options, removes it from hand, and returns it
        rnd = random.randrange(0, len(options))
        card = options[rnd]
        self.hand.remove(card)
        return card
    
    def playBid(self, ban, handSize, trump): #picks a random number from 0 to 13
        rnd = ban
        while rnd == ban:
            rnd = random.randrange(0, handSize)
        self.bid = rnd

    def __str__(self):
        string = self.name + ": "
        string += self.hand.__str__()
        return string