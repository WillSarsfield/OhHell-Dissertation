from Player import Player
from Deck import Deck
from GameTree import GameTree
import numpy as np
import random
import math
import time

class BestAgent(Player):
    
    def __init__(self, name):
        super().__init__(name)
        
    def updateCardsInDeck(self, cards):
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def playOption(self, options, cardsPlayed, trump, players, bids, scores):
        self.updateCardsInDeck(cardsPlayed)
        if len(options) == 1:
            choice = options[0]
            self.hand.remove(choice)
            return choice
        time_limit = 10
        time_start = time.time()
        iterations = 1000
        wins = [0 for _ in options]
        samples = 0
        while time.time() - time_start < time_limit:
            samples += 1
            # make game tree
            game_tree = GameTree(parent = None, hands = [self.hand.getCards()], cards_played=cardsPlayed, players = players, bids = bids, scores = scores, trump=trump, max_depth=12)
            game_tree.determinize(self.cardsInDeck)
            for _ in range(iterations):
                selection = game_tree.select_child()
                expansion = selection.expand()
                simulated_value = expansion.simulate()
                expansion.backpropagate(simulated_value)
            for x, child in enumerate(game_tree.children):
                wins[x] += child.wins/child.visits
        print(self.cardsInDeck)
        print(f"Scores: {scores}")
        for i, win in enumerate(wins):
            print(f"({options[i]}: {win/samples})", end = " ")
        print(f"\nSamples: {samples}")
        choice = options[wins.index(max(wins))]
        self.hand.remove(choice)
        return choice

    def playBid(self, ban, handSize, trump, lead, players, bids):
        self.cardsInDeck = Deck()
        self.updateCardsInDeck(self.hand.getCards())
        samples = 30
        iterations = 1000
        wins = np.zeros(handSize)
        scores = [0 for _ in range(players)]
        for i in range(samples):
            # make game tree
            game_tree = GameTree(parent = None, hands = [self.hand.getCards()], scores=scores, players = players, trump=trump, max_depth=12)
            game_tree.determinize(self.cardsInDeck)
            for j in range(iterations):
                selection = game_tree.select_child()
                expansion = selection.expand()
                simulated_value = expansion.simulate()
                expansion.backpropagate(simulated_value)
            for x, child in enumerate(game_tree.children): # gets average score over cards from random playouts
                wins[x] += child.wins/child.visits
        if lead: # can choose so should choose highest expected score
            bid = np.max(wins)/samples
        else: # can't choose so finds the average expected score
            bid = np.mean(wins)/samples
        print(bid)
        npbids = np.array(bids)
        if len(bids) == players - 1:
            if np.sum(npbids) > handSize: # if over bid round down
                if math.floor(bid) == ban: #if rounding down hits the ban, round up
                    bid = math.ceil(bid)
                else:
                    bid = math.floor(bid)
            else: # if under bid
                if math.ceil(bid) == ban: #if rounding up hits the ban, round down
                    bid = math.floor(bid)
                else:
                    bid = math.ceil(bid)
        else:
            bid = round(bid)
        self.bid = bid