from Deck import Deck
from Hand import Hand
from Player import Player

deck = Deck()

deck.shuffle()

print("Deck:")


print(deck)

print("Hand:")

playerList = []
for i in range(0,4): 
    hand = Hand(deck.makeHand())
    player = Player(str(i+1))
    player.makeHand(hand)
    playerList.append(player)

for player in playerList:
    print(player)
    player.sortHand()
    print(player)
    player.shuffleHand()
    print(player)

