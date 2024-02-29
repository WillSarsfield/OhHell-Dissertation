from GameTree import GameTree
from Card import Card
from Deck import Deck
import time
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def run():
    cardsInDeck = Deck()
    players = 4
    bids = [0,1,2,3]
    current_player = 3
    iterations = 2000
    hands = [[Card(9,0),Card(2,1),Card(6,1),Card(12,2)],
             [Card(14,0),Card(3,1),Card(6,2),Card(6,3)],
             [Card(10,0),Card(13,0),Card(14,1),Card(12,3)],
             [Card(11,0),Card(12,0),Card(10,3),Card(14,3)]]
    wins = [0 for _ in hands[current_player]]
    for i, h in enumerate(hands):
        print(f"player {i + 1} bid {bids[i]} with:", end = "")
        for c in h:
            print(c, end= " ")
            if i == current_player:
                cardsInDeck.removeCard(c)
        print()
    print(cardsInDeck)
    cardsPlayed = []
    scores = [0,0,0,0]
    trump = 0
    print(f"Tree if player {current_player+1} was leading:")
    game_tree = GameTree(parent = None, hands = hands, cards_played=cardsPlayed, players = players, bids = bids, scores = scores, trump=trump, current_player=current_player, max_depth=12)
    for _ in range(iterations):
        selection = game_tree.select_child()
        if selection.terminate:
            break
        expansion = selection.expand()
        simulated_value = expansion.simulate()
        expansion.backpropagate(simulated_value)
    for x, child in enumerate(game_tree.children):
        wins[x] += child.wins/child.visits
    print(game_tree.__str__(4))
    for i, c in enumerate(hands[current_player]):
        print(f"{c}: {wins[i]}")

if __name__ == "__main__":
    run()