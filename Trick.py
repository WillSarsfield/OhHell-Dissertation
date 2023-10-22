from Card import Card

def trick(trump, first, cardList):
        winner = first
        winnerVal = cardList[0].getValue()
        winnerSuit = cardList[0].getSuit()
        if cardList[0].getSuit() == trump:
            winnerTrumping = True
        else:
            winnerTrumping = False
        i = 0
        for card in cardList:
            if card.getSuit() == cardList[0].getSuit():
                  if card.getValue() > winnerVal:
                        winner = (first + i) % 4
                        winnerVal = card.getValue()
            elif card.getSuit() == trump:
                if card.getValue() > winnerVal:
                    winner = (first + i) % 4
                    winnerVal = card.getValue()
                    winnerTrumping = True
                elif not winnerTrumping:
                    winner = (first + i) % 4
                    winnerVal = card.getValue()
                    winnerTrumping = True
                    winnerSuit = trump
            i += 1
        winnerCard = Card(winnerVal, winnerSuit)
        print("Card that won:")
        print(winnerCard)
        return winner