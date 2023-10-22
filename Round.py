from Deck import Deck
from Player import Player
from Hand import Hand
import Trick

class Round:
    def __init__(self, trump, first, playerList) -> None:
        suitDict = {
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
            hand = Hand(deck.makeHand())
            hand.sort()
            player.makeHand(hand)
            print(player)
        ###
        #bidding phase
        bidTotal = 0
        for i in range(0, len(playerList)):
            if i != len(playerList) - 1:
                playerList[i].playRandomBid(14)
                bidTotal += playerList[i].getBid()
                print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))
            else:
                if bidTotal < 14:
                    playerList[i].playRandomBid(13 - bidTotal)
                else:
                    playerList[i].playRandomBid(14)
                print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))

        for i in range(0, 13):
            cardList = []
            print("first = " + str(first + 1))
            options = playerList[first].getOptions()#lead player makes choice
            print("player " + str(first + 1) + "'s turn:")
            leadCard = playerList[first].playRandomOption(options)
            print(leadCard)
            cardList.append(leadCard)
            for i in range(first + 1 , first + 4):
                options = playerList[i % 4].getOptions(leadCard.getSuit())
                print("player " + str((i % 4) + 1) + "'s turn:")
                card = playerList[i % 4].playRandomOption(options)
                print(card)
                cardList.append(card)
            first = Trick.trick(trump, first, cardList)
            playerList[first].addRoundScore(1)
        for player in playerList:
            if player.getRoundScore() == player.getBid():
                player.addScore(10 + player.getRoundScore())
            else:
                player.addScore(player.getRoundScore())

