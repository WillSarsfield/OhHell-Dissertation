from GameTree import GameTree
from Deck import Deck

deck1 = Deck()
deck1.shuffle()
hands = []
unseen = []
for i in range (0,4):
    hands.append(deck1.makeHand(4))
    if i > 0:
        unseen.append(hands[i])

unseen = [card for hand in unseen for card in hand]
deck1.cardList = unseen
for i, hand in enumerate(hands):
    print(f"Player {i+1}: ", end = " ")
    for card in hand:
        print(card, end = " ")
    print()

for card in unseen:
    print(card, end= " ")
print()
iterations = 1000
samples = 10
for j in range(samples):
    game_tree = GameTree(parent = None, hands = [hands[0]], scores=[0,0,0,0], bids=[1,1,1,0], players = 4, trump=0, max_depth=12)
    game_tree.determinize(deck1)
    for i, hand in enumerate(game_tree.hands):
        print(f"Player: {i+1}", end=" ")
        for card in hand:
            print(card, end= " ")
        print()
    for i in range(iterations):
        selection = game_tree.select_child(4-(3*(i/iterations)**2))
        if selection.terminate:
            break
        expansion = selection.expand()
        simulated_value = expansion.simulate()
        expansion.backpropagate(simulated_value)
    print(game_tree.__str__(1))
