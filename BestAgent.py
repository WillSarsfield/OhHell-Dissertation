from Player import Player
from Deck import Deck
from GameTree import GameTree
import numpy as np
import random
import math
import time
from scipy import stats

class BestAgent(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.cardsInDeck = Deck()
    
    def resetCardsInDeck(self, cards):
        self.cardsInDeck = Deck()
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def updateCardsInDeck(self, cards):
        if not self.cardsInDeck.cardList:
            self.cardsInDeck = Deck()
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def playOption(self, options, cardsPlayed, trump, players, bids, scores):
        self.updateCardsInDeck(cardsPlayed)
        if len(options) == 1:
            choice = options[0]
            self.hand.remove(choice)
            return choice
        time_limit = 5
        time_start = time.time()
        iterations = 5000
        wins = [0 for _ in options]
        samples = 0
        win_count = 0
        while time.time() - time_start < time_limit:
            winner_index = 0
            samples += 1
            # make game tree
            game_tree = GameTree(parent = None, hands = [self.hand.getCards()], cards_played=cardsPlayed, players = players, bids = bids, scores = scores, trump=trump, max_depth=12)
            game_tree.determinize(self.cardsInDeck)
            for _ in range(iterations):
                selection = game_tree.select_child()
                if selection.terminate:
                    break
                expansion = selection.expand()
                simulated_value = expansion.simulate()
                expansion.backpropagate(simulated_value)
            for x, child in enumerate(game_tree.children):
                wins[x] += child.wins/child.visits
            #     print(f"{child.card_choice} = {round(wins[x]/samples, 3)}", end = "")
            #     if x == 7:
            #         print()
            # print()
            if wins.index(max(wins)) != winner_index:
                win_count = 0
                winner_index = wins.index(max(wins))
            else:
                win_count += 1
                if win_count > 9:
                    print(f"{options[wins.index(max(wins))]} has been the best for 10 determinizations")
                    break
        print(f"Scores: {scores}")
        print(f"\nSamples: {samples}")
        choice = options[wins.index(max(wins))]
        self.hand.remove(choice)
        return choice

    def playBid(self, ban, handSize, trump, lead, players, bids):
        current_bid = 0
        self.updateCardsInDeck(self.hand.getCards())
        print(self.cardsInDeck)
        time_limit = 5
        time_start = time.time()
        iterations = 5000
        wins = np.zeros(handSize)
        scores = [0 for _ in range(players)]
        samples = 0
        bid_count = 0
        while time.time() - time_start < time_limit:
            samples += 1
            # make game tree
            game_tree = GameTree(parent = None, hands = [self.hand.getCards()], scores=scores, players = players, trump=trump, max_depth=12)
            game_tree.determinize(self.cardsInDeck)
            for j in range(iterations):
                selection = game_tree.select_child()
                if selection.terminate:
                    break
                expansion = selection.expand()
                simulated_value = expansion.simulate()
                expansion.backpropagate(simulated_value)
            for x, child in enumerate(game_tree.children): # gets average score over cards from random playouts
                wins[x] += child.wins/child.visits
            bid = np.mean(wins)/samples
            if round(bid) == round(current_bid):
                bid_count+=1
                if bid_count > 9:
                    print(f"{round(bid)} has been the same bid for 10 determinizations")
                    break
            else:
                bid_count = 0
            current_bid = bid
            #     print(f"{child.card_choice} = {round((child.wins/child.visits)/samples, 3)} ", end = " ")
            #     if x == 7:
            #         print()
            # print()
            # for x, child in enumerate(game_tree.children): # gets average score over cards from random playouts
            #     print(f"{child.card_choice} = {round((wins[x])/samples, 3)} ", end = " ")
            #     if x == 7:
            #         print()
            # print()
        bid = np.mean(wins)/samples
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
        print(bid)
        self.bid = bid