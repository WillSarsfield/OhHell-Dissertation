from Player import Player
from Deck import Deck
import random

class InformedPlayer(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.cardsInDeck = Deck()
        
    def updateCardsInDeck(self, cards):
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def playOption(self, options, cardsPlayed, trump, players):
        self.updateCardsInDeck(cardsPlayed)
        #print(f"cards left: {self.cardsInDeck}")
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
                if winningOptions: # if a choice can be made that wins, choose the most likely to win given the remaining cards
                    winningProbabilities = [self.getWinningProbabilityPlay(option, cardsPlayed[0].getSuit(), trump) for option in winningOptions]
                    print(winningProbabilities)
                    if len(cardsPlayed) == players - 1:
                        choice = winningOptions[winningProbabilities.index(min(winningProbabilities))]
                    else:
                        choice = winningOptions[winningProbabilities.index(max(winningProbabilities))]
                    for option in winningOptions:
                        print(option, end = " ")
                    print()
                    print(choice)
                else: # if no choices can be made that win, choose the least likely to win given the remaining cards
                    winningProbabilities = [self.getWinningProbabilityPlay(option, cardsPlayed[0].getSuit(), trump) for option in options]
                    print(winningProbabilities)
                    choice = options[winningProbabilities.index(min(winningProbabilities))]
                    for option in options:
                        print(option, end = " ")
                    print()
                    print(choice)
            if self.roundScore == self.bid: # if bid is reached then keep losing
                if losingOptions: # if there is an option to lose, then lose by throwing the most valuable card away
                    winningProbabilities = [self.getWinningProbabilityPlay(option, cardsPlayed[0].getSuit(), trump) for option in losingOptions]
                    print(winningProbabilities)
                    if len(cardsPlayed) == players - 1:
                        choice = losingOptions[winningProbabilities.index(max(winningProbabilities))]
                    else:
                        choice = losingOptions[winningProbabilities.index(min(winningProbabilities))]
                    for option in losingOptions:
                        print(option, end = " ")
                    print()
                    print(choice)
                else: # if there is no choice but to win, then win
                    rnd = random.randrange(0, len(options))
                    choice = options[rnd]
        else: # if leading play the best or worst option depending on the remain cards
            winningProbabilities = [self.getWinningProbabilityPlay(option, option.getSuit(), trump) for option in options]
            print(winningProbabilities)
            bestOption = options[winningProbabilities.index(max(winningProbabilities))]
            worstOption = options[winningProbabilities.index(min(winningProbabilities))]
            for option in options:
                print(option, end = " ")
            print()
            print(bestOption)
            print(worstOption)
            if self.roundScore < self.bid or self.roundScore > self.bid: # if not at the bid then keep winning
                    choice = bestOption
            if self.roundScore == self.bid: # if bid is reached then keep losing
                choice = worstOption
        self.hand.remove(choice)
        return choice

    def getWinningProbabilityPlay(self, card, leadSuit, trump):
        winCount = 0
        # chance card beats other cards
        for c in self.cardsInDeck.getCards():
                if card.beats(c, leadSuit, trump):
                    winCount += 1
        
        return (winCount/len(self.cardsInDeck.getCards()))
    
    def getWinningProbabilityBid(self, card, lead, trump):
        winCount = 0
        # chance card beats other cards
        if lead:
            for c in self.cardsInDeck.getCards():
                if card.beats(c, card.getSuit(), trump):
                    winCount += 1
        else:
            for c in self.cardsInDeck.getCards():
                if card.beats(c, c.getSuit(), trump):
                    winCount += 1
        # chance card wins if in suit
        # sameSuitCards = 0
        # winSuitCards = 0
        # for c in self.cardsInDeck.getCards():
        #     if c.getSuit() == card.getSuit():
        #         sameSuitCards += 1
        #         if c.getValue() < card.getValue():
        #             winSuitCards += 1
                
        
        return (winCount/len(self.cardsInDeck.getCards())) #* (winSuitCards/sameSuitCards)
    
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

    def playBid(self, ban, handSize, trump, lead, players):
        self.cardsInDeck = Deck()
        self.updateCardsInDeck(self.hand.getCards())
        bid = ban
        while bid == ban:
            bid = 0
            print([self.getWinningProbabilityBid(card, lead, trump) for card in self.hand.getCards()])
            for card in self.hand.getCards():
                print(card, end = " ")
            print()
            for card in self.hand.getCards():
                if self.getWinningProbabilityBid(card, lead, trump) > 0.7:
                    bid += 1
                    print(f"{card}: {self.getWinningProbabilityBid(card, lead, trump)}")
        self.bid = bid