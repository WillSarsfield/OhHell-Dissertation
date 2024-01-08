from GameTree import GameTree
from Player import Player
from Deck import Deck
from Hand import Hand

playerList = []
for i in range(4):
    player = Player(f"Test{i+1}")
    playerList.append(player)

deck = Deck()
deck.shuffle()

for player in playerList: 
    hand = Hand(deck.makeHand(13))
    hand.sort()
    player.makeHand(hand)
    print(player)

player1_hand = playerList[0].getHand().getCards()
unseen = Deck()
for card in player1_hand:
    unseen.removeCard(card)
game_tree = GameTree(parent = None, hands = [player1_hand], players = 4, bids = [1,2,3,4], scores=[0,0,0,0], trump=0, current_player=0, initial_player = 0, max_depth = 12)
game_tree.determinize(unseen)

for i in range(10000):
    selection = game_tree.select_child()
    expansion = selection.expand()
    simulated_value = expansion.simulate()
    expansion.backpropagate(simulated_value)
print(game_tree.__str__(1))