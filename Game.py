from Player import Player
from InformedPlayer import InformedPlayer
from BestAgent import BestAgent
from Deck import Deck
from Hand import Hand
from Card import Card
import math
import sys, os

#Game class that when called plays the number of rounds specified

class Game:
    def __init__(self, rounds, players, playersStrength, handSize = None, verbose=True, optimisations = [], best_weights=[]) -> None:
        self.players = players #number of players
        self.playerList = []
        if handSize:
            self.handSize = handSize
        else:
            self.handSize = math.floor(52/players)
        self.displayCards = []
        self.winningCards = []
        self.currentLead = []
        self.currentBids = []
        self.trumps = []
        if not verbose:
            sys.stdout = open(os.devnull, 'w', encoding="utf-8")
        for i in range(0, self.players):
            if playersStrength[i] == 0:
                player = Player("player " + str(i+1))#make players with names
            elif playersStrength[i] == 1:
                player = InformedPlayer("player " + str(i+1), optimisations)#make informed players with names
            elif playersStrength[i] == 2:
                player = BestAgent(f"player {i+1}") #make best agents with names

            self.playerList.append(player)#add to list of players
        for i in range(0, rounds):#run round function rounds times
            self.round(i % 4, i % self.players, self.handSize)#change the player going first and the trump each time = {0,...,3}
            for player in self.playerList:
                print(f"{player.getName()}, score this round: {player.getRoundScore()}, overall score: {player.getScore()}")
                player.addRoundScore(-player.getRoundScore())
    
    def getPlayers(self):#return player scores for statistics overview
        return self.playerList
    
    def getCardsPlayed(self):
        return self.displayCards
    
    def getWinningCards(self):
        return self.winningCards
    
    def getCurrentLead(self):
        return self.currentLead
    
    def getCurrentBids(self):
        return self.currentBids
    
    def getTrumps(self):
        return self.trumps

    def round(self, trump, first, handSize):
        suitDict = { #translate suit value to symbol
            0: "♥",
            1: "♦",
            2: "♠",
            3: "♣"
        }
        print()
        print("Trumps = " + suitDict[trump])
        self.trumps.append(trump)
        deck = Deck()#make deck
        deck.shuffle()#shuffle deck

        #deal cards to players
        for player in self.playerList: 
            hand = Hand(deck.makeHand(handSize))
            hand.sort()
            player.makeHand(hand)
            print(player)
        ###
        #bidding phase
        bidTotal = 0
        bids = []
        for i in range(first , first + len(self.playerList)):
            if deck.cardList: #update cards not used in the round, consistent for each player
                self.playerList[i % len(self.playerList)].resetCardsInDeck(deck.cardList)
            if i != first + len(self.playerList) - 1:
                if i == first:
                    self.playerList[i % len(self.playerList)].playBid(handSize + 1, handSize, trump, True, len(self.playerList), bids) #can make bid, argument passed represents a bid that is banned (14 passed as it is an unbiddable number)
                else:
                    self.playerList[i % len(self.playerList)].playBid(handSize + 1, handSize, trump, False, len(self.playerList), bids)
                bidTotal += self.playerList[i % len(self.playerList)].getBid()
                print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                bids.append(self.playerList[i % len(self.playerList)].getBid())
            else:
                if bidTotal < handSize + 1: #calculates the bid that is banned for the final player
                    self.playerList[i % len(self.playerList)].playBid(handSize - bidTotal, handSize, trump, False, len(self.playerList), bids)
                else:
                    self.playerList[i % len(self.playerList)].playBid(handSize + 1, handSize, trump, False, len(self.playerList), bids)
                print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                bids.append(self.playerList[i % len(self.playerList)].getBid())

        self.displayCards.append([])
        self.winningCards.append(None)
        self.currentLead.append(first)
        self.currentBids.append(bids)
        for player in self.playerList:
                player.addScoreHistory(player.getScore())
        for i in range(0, handSize):
            scores = [0 for _ in range(len(self.playerList))]
            for j, player in enumerate(self.playerList):#save hand in history for display later
                saveCards = []
                scores[j] = player.getRoundScore()
                for card in player.getHand().getCards():
                    saveCards.append(card)
                player.addHandHistory(saveCards)
            cardList = [] #cardlist the trick will be passed into
            print("first = " + str(first + 1))
            options = self.playerList[first].getOptions() #lead player collects all the possible plays it can make
            print("player " + str(first + 1) + "'s turn:")
            leadCard = self.playerList[first].playOption(options, cardList, trump, len(self.playerList), bids, scores) #lead player chooses a play from its options
            print(leadCard)
            cardList.append(leadCard) #lead card is added to the trick
            for i in range(first + 1 , first + len(self.playerList)): #iterate over remaining players choices in order ascending from first player
                options = self.playerList[i % len(self.playerList)].getOptions(leadCard.getSuit()) #player collects all the possible plays it can make
                print("player " + str((i % len(self.playerList)) + 1) + "'s turn:")
                card = self.playerList[i % len(self.playerList)].playOption(options, cardList, trump, len(self.playerList), bids, scores) #player chooses a play from its options
                print(card)
                cardList.append(card) #card played added to list
            for player in self.playerList:
                player.updateCardsInDeck(cardList)
            self.displayCards.append(cardList) #save cards in the trick to be displayed
            first = self.trick(trump, first, cardList, len(self.playerList)) #trick winner decided, index of the player who won is returned
            self.currentLead.append(first)
            self.playerList[first].addRoundScore(1) #update winning player's score
            for player in self.playerList:
                player.addScoreHistory(player.getScore() + player.getRoundScore())
        for player in self.playerList: #awards bonus points to any player who matched their bid at the end of the round
            player.addHandHistory([])
            if player.getRoundScore() == player.getBid():
                player.addRoundScore(10)
                player.addScore(player.getRoundScore())
                player.updateBidsMade()
            else:
                player.addScore(player.getRoundScore())
            player.addScoreHistory(player.getScore())

    def trick(self, trump, first, cardList, players):
        winner = first #winner is set as the first player to start
        winnerCard = cardList[0]
        leadSuit = winnerCard.getSuit()
        i = 0 #count needed to format player turns correctly
        for card in cardList:
            if card.beats(winnerCard, leadSuit, trump):
                winner = (first + i) % players #set winner to current index of card played
                winnerCard = card   
            i += 1
        self.winningCards.append(winnerCard)
        print("Card that won:")
        print(winnerCard)
        return winner #return the index of the player that won

