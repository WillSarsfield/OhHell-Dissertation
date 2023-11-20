from Player import Player
import random

class InformedPlayer(Player):
    
    def playOption(self, options, trump, roundScore, cardsPlayed):
        if len(options) == 1:
            return options[0]
        rnd = random.randrange(0, len(options))
        if cardsPlayed:
            for card in cardsPlayed:
                for option in options:
                    if card.getValue() > options.getValue() and options.getSuit() != trump:
                        pass
        card = options[rnd]
        self.hand.remove(card)
        return card

    def playBid(self, ban, handSize, trump):
        bid = ban
        while bid == ban:
            bid = 0
            for card in self.hand.getCards():
                rnd = random.randrange(0, handSize)
                if rnd <= card.getValue():
                    bid += 1
                elif card.getSuit() == trump:
                    bid += 1
        return bid