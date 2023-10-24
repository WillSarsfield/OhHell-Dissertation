from Deck import Deck
from Hand import Hand
import Trick

def round(trump, first, playerList):
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
        hand = Hand(deck.makeHand())
        hand.sort()
        player.makeHand(hand)
        print(player)
    ###
    #bidding phase
    bidTotal = 0
    for i in range(0, len(playerList)):
        if i != len(playerList) - 1:
            playerList[i].playRandomBid(14) #can make random bid, argument passed represents a bid that is banned (14 passed as it is an unbiddable number)
            bidTotal += playerList[i].getBid()
            print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))
        else:
            if bidTotal < 14: #calculates the bid that is banned for the final player
                playerList[i].playRandomBid(13 - bidTotal)
            else:
                playerList[i].playRandomBid(14)
            print("player " + str(i+1) + " bid: " + str(playerList[i].getBid()))

    for i in range(0, 13):
        cardList = [] #cardlist the trick will be passed into
        print("first = " + str(first + 1))
        options = playerList[first].getOptions() #lead player collects all the possible plays it can make
        print("player " + str(first + 1) + "'s turn:")
        leadCard = playerList[first].playRandomOption(options) #lead player chooses a play from its options
        print(leadCard)
        cardList.append(leadCard) #lead card is added to the trick
        for i in range(first + 1 , first + 4): #iterate over remaining players choices in order ascending from first player
            options = playerList[i % 4].getOptions(leadCard.getSuit()) #player collects all the possible plays it can make
            print("player " + str((i % 4) + 1) + "'s turn:")
            card = playerList[i % 4].playRandomOption(options) #player chooses a play from its options
            print(card)
            cardList.append(card) #card played added to list
        first = Trick.trick(trump, first, cardList) #trick winner decided, index of the player who won is returned
        playerList[first].addRoundScore(1) #update winning player's score
    for player in playerList: #awards bonus points to any player who matched their bid at the end of the round
        if player.getRoundScore() == player.getBid():
            player.addScore(10 + player.getRoundScore())
        else:
            player.addScore(player.getRoundScore())

