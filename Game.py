from Player import Player
from Deck import Deck
from Hand import Hand
from Card import Card
import math

#Game class that when called plays the number of rounds specified

class Game:
    def __init__(self, rounds, players) -> None:
        self.players = players #number of players
        self.playerList = []
        self.handSize = math.floor(52/players)
        for i in range(0, self.players):
            player = Player("player " + str(i+1))#make players with names
            self.playerList.append(player)#add to list of players
        for i in range(0, rounds):#run round function rounds times
            self.round(i % 4, i % self.players, self.playerList, self.handSize)#change the player going first and the trump each time = {0,...,3}
    
    def getPlayers(self):#return player scores for statistics overview
        return self.playerList
    
    def round(self, trump, first, playerList, handSize):
        suitDict = { #translate suit value to symbol
            0: "♥",
            1: "♦",
            2: "♠",
            3: "♣"
        }
        print()
        print("Trumps = " + suitDict[trump])
        deck = Deck()#make deck
        deck.shuffle()#shuffle deck

        #deal cards to players
        for player in playerList: 
            hand = Hand(deck.makeHand(handSize))
            hand.sort()
            player.makeHand(hand)
            print(player)
        ###
        #bidding phase
        bidTotal = 0
        for i in range(0, len(playerList)):
            if i != len(playerList) - 1:
                playerList[i].playRandomBid(handSize + 1, handSize) #can make random bid, argument passed represents a bid that is banned (14 passed as it is an unbiddable number)
                bidTotal += playerList[i].getBid()
                print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))
            else:
                if bidTotal < 14: #calculates the bid that is banned for the final player
                    playerList[i].playRandomBid(handSize - bidTotal, handSize)
                else:
                    playerList[i].playRandomBid(handSize + 1, handSize)
                print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))

        for i in range(0, handSize):
            cardList = [] #cardlist the trick will be passed into
            print("first = " + str(first + 1))
            options = playerList[first].getOptions() #lead player collects all the possible plays it can make
            print("player " + str(first + 1) + "'s turn:")
            leadCard = playerList[first].playRandomOption(options) #lead player chooses a play from its options
            print(leadCard)
            cardList.append(leadCard) #lead card is added to the trick
            for i in range(first + 1 , first + len(playerList)): #iterate over remaining players choices in order ascending from first player
                options = playerList[i % len(playerList)].getOptions(leadCard.getSuit()) #player collects all the possible plays it can make
                print("player " + str((i % len(playerList)) + 1) + "'s turn:")
                card = playerList[i % len(playerList)].playRandomOption(options) #player chooses a play from its options
                print(card)
                cardList.append(card) #card played added to list
            first = self.trick(trump, first, cardList, len(playerList)) #trick winner decided, index of the player who won is returned
            playerList[first].addRoundScore(1) #update winning player's score
        for player in playerList: #awards bonus points to any player who matched their bid at the end of the round
            if player.getRoundScore() == player.getBid():
                player.addScore(10 + player.getRoundScore())
            else:
                player.addScore(player.getRoundScore())

    def trick(self, trump, first, cardList, players):
        winner = first #winner is set as the first player to start
        winnerVal = cardList[0].getValue()
        winnerSuit = cardList[0].getSuit()
        if cardList[0].getSuit() == trump: #registers if the lead card is a trump
            winnerTrumping = True
        else:
            winnerTrumping = False
        i = 0 #count needed to format player turns correctly
        for card in cardList:
            if card.getSuit() == trump: #if contesting card is a trump
                if card.getValue() > winnerVal: #if the value is higher than the current they are winning
                    winner = (first + i) % players #set winner to current index of card played
                    winnerVal = card.getValue()
                    winnerTrumping = True #set up flag that the winner is trumping
                elif not winnerTrumping: #if current winner is not a trump then current card trumps
                    winner = (first + i) % players
                    winnerVal = card.getValue()
                    winnerTrumping = True #set up flag that the winner is trumping
                winnerSuit = trump #update winning card suit
            elif card.getSuit() == cardList[0].getSuit(): #if card is the same as current suit
                  if card.getValue() > winnerVal: #and that card is higher value than the current winner
                        winner = (first + i) % players
                        winnerVal = card.getValue()
            i += 1
        winnerCard = Card(winnerVal, winnerSuit)
        print("Card that won:")
        print(winnerCard)
        return winner #return the index of the player that won

