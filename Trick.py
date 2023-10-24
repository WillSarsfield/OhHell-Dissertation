from Card import Card

def trick(trump, first, cardList):
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
                    winner = (first + i) % 4 #set winner to current index of card played
                    winnerVal = card.getValue()
                    winnerTrumping = True #set up flag that the winner is trumping
                elif not winnerTrumping: #if current winner is not a trump then current card trumps
                    winner = (first + i) % 4
                    winnerVal = card.getValue()
                    winnerTrumping = True #set up flag that the winner is trumping
                winnerSuit = trump #update winning card suit
            elif card.getSuit() == cardList[0].getSuit(): #if card is the same as current suit
                  if card.getValue() > winnerVal: #and that card is higher value than the current winner
                        winner = (first + i) % 4
                        winnerVal = card.getValue()
            i += 1
        winnerCard = Card(winnerVal, winnerSuit)
        print("Card that won:")
        print(winnerCard)
        return winner #return the index of the player that won