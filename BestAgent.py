from Player import Player
from Deck import Deck
import random

class BestAgent(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.cardsInDeck = Deck()
        
    def updateCardsInDeck(self, cards):
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def playOption(self, options, cardsPlayed, trump, players):
        # make game tree
        # update game tree with n random playouts
        # select best option
        choice = random.choice(options)
        return choice

    def playBid(self, ban, handSize, trump, lead, players):
        # make game tree
        # update game tree with n random playouts
        # select best option
        bid = ban
        while bid == ban:
            bid = random.randint(0, handSize)