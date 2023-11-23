from Player import Player
import random

class InformedPlayer(Player):
    
    def playOption(self, options, cardsPlayed, trump):
        if len(options) == 1:
            choice = options[0]
            self.hand.remove(choice)
            return choice
        choice = None
        winningOptions = []
        losingOptions = []
        if cardsPlayed: # if not leading
            winningOptions = self.getWinningOptions(options, cardsPlayed, trump)
            losingOptions = self.getLosingOptions(options, cardsPlayed, trump)
            if self.roundScore < self.bid or self.roundScore > self.bid: # if not at the bid then keep winning
                if winningOptions:
                    rnd = random.randrange(0, len(winningOptions))
                    choice = winningOptions[rnd]
                else:
                    rnd = random.randrange(0, len(options))
                    choice = options[rnd]
            if self.roundScore == self.bid: # if bid is reached then keep losing
                if losingOptions:
                    rnd = random.randrange(0, len(losingOptions))
                    choice = losingOptions[rnd]
                else:
                    rnd = random.randrange(0, len(options))
                    choice = options[rnd]
        else: # if leading
            bestOption = options[0]
            worstOption = options[0]
            for option in options:
                if option.getValue() > bestOption.getValue():
                    bestOption = option
                if option.getValue() < worstOption.getValue():
                    worstOption = option
            if self.roundScore < self.bid or self.roundScore > self.bid: # if not at the bid then keep winning
                    choice = bestOption
            if self.roundScore == self.bid: # if bid is reached then keep losing
                choice = worstOption
    
        self.hand.remove(choice)
        return choice
    
    def getWinningOptions(self, options, cardsPlayed, trump):
        winningCard = cardsPlayed[0]
        if len(cardsPlayed) > 1:
            for card in cardsPlayed:
                if trump == winningCard.getSuit() and card.getSuit() == trump and card.getValue() > winningCard.getValue():
                    winningCard = card
                elif trump != winningCard.getSuit():
                    if card.getSuit() == winningCard.getSuit() and card.getValue() > winningCard.getValue():
                        winningCard = card
                    elif card.getSuit() == trump:
                        winningCard = card
        winningOptions = []
        for option in options:
            if trump == winningCard.getSuit() and option.getSuit() == trump and option.getValue() > winningCard.getValue():
                    winningOptions.append(option)
            elif trump != winningCard.getSuit():
                if option.getSuit() == winningCard.getSuit() and option.getValue() > winningCard.getValue():
                    winningOptions.append(option)
                elif option.getSuit() == trump:
                    winningOptions.append(option)
        return winningOptions
    
    def getLosingOptions(self, options, cardsPlayed, trump):
        winningOptions = self.getWinningOptions(options, cardsPlayed, trump)
        return [option for option in options if option not in winningOptions]

    def playBid(self, ban, handSize, trump):
        bid = ban
        while bid == ban:
            bid = 0
            for card in self.hand.getCards():
                rnd = random.randrange(7, handSize)
                if rnd <= card.getValue():
                    bid += 1
                elif card.getSuit() == trump and card.getValue() > 7:
                    bid += 1
        self.bid = bid