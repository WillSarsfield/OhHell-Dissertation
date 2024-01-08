from Player import Player
from Deck import Deck
from GameTree import GameTree
import random

class BestAgent(Player):
    
    def __init__(self, name, player_pos):
        super().__init__(name)
        self.cardsInDeck = Deck()
        self.player_pos = player_pos
        
    def updateCardsInDeck(self, cards):
        for card in cards:
            self.cardsInDeck.removeCard(card)

    def playOption(self, options, cardsPlayed, trump, players, bids, scores):
        samples = 13
        iterations = 1000
        wins = [0 for _ in options]
        for i in range(samples):
            # make game tree
            game_tree = GameTree(parent = None, hands = [self.hand.getCards()], cards_played=cardsPlayed, players = players, bids = bids, scores = scores, trump=trump, current_player=self.player_pos, initial_player=self.player_pos, max_depth=12)
            game_tree.determinize(self.cardsInDeck)
            for j in range(iterations):
                selection = game_tree.select_child()
                expansion = selection.expand()
                simulated_value = expansion.simulate()
                expansion.backpropagate(simulated_value)
            for x, child in enumerate(game_tree.children):
                wins[x] += child.wins
        choice = options[wins.index(max(wins))]
        return choice

    def playBid(self, ban, handSize, trump, lead, players):
        # make game tree
        # update game tree with n random playouts
        # select best option
        bid = ban
        while bid == ban:
            bid = random.randint(0, handSize)