import random
import math
import time
import numpy as np
import copy
from collections import defaultdict

class GameTree:

    def __init__(self, parent = None, hands = [], cards_played = [], scores = [], bids = None, players = None, trump = None, current_player = 0, initial_player = 0, max_depth = None, depth = 0) -> None:
        self.parent = parent
        self.children = []
        self.hands = hands # cards player has 
        self.cards_played = cards_played # cards that have been played in the trick
        self.scores = scores # current scores of players (in order)
        self.bids = bids # current bids of players (in order)
        self.players = players # number of players
        self.trump = trump # trump suit for the round
        self.i = current_player # player whose turn it currently is
        self.initial_player = initial_player # player who we're building the tree for
        self.max_depth = max_depth
        self.depth = depth
        self.visits = 0 # times node was visited
        self.wins = 0 # score of node
        self.choices = []
        if len(self.cards_played) == self.players or not self.cards_played:
            self.choices = self.hands[self.i]
        else:
            self.choices = self.get_choices(self.hands[self.i], self.cards_played[0])
        self.unprocessed_choices = copy.deepcopy(self.choices)
        if self.depth >= self.max_depth or not self.choices: # if depth is exceeded or player has no moves (round finished) then return
            return

    def get_choices(self, hand, leadCard):
        choices = []
        for card in hand: #add cards of the same suit as the lead to the options
            if card.getSuit() == leadCard.getSuit():
                choices.append(card)
        if not choices: #if no cards with the same suit as the lead, all cards are options
            choices = hand
        return choices

    def determinize(self, cardsInDeck):
        unseen = copy.deepcopy(cardsInDeck)
        # already played a card in trick so must deduct cards from initial players hands
        indent = 0
        if self.cards_played:
            indent = len(self.cards_played)
        # select random distribution of unseen cards for other players to have
        for _ in range(self.players - 1):
            if indent > 0:
                random_hand = random.sample(unseen.getCards(), k=len(self.hands[self.i]) - 1)
            else:
                random_hand = random.sample(unseen.getCards(), k=len(self.hands[self.i]))
            indent -= 1
            self.hands.append(random_hand)
            # remove selected cards from unseen
            for card in random_hand:
                unseen.removeCard(card)

    def select_child(self, exploration_weight=1.4):
        """Select a child node using UCT (Upper Confidence Bound for Trees) formula"""
        # if no children, select itself
        if not self.children:
            return self
        log_total_visits = 0
        for child in self.children:
            log_total_visits += child.visits
        log_total_visits = math.log(log_total_visits)
        # if all choices do not have a node, select itself
        if len(self.children) < len(self.choices):
            return self

        def uct_value(child):
            exploitation_term = child.wins / child.visits
            exploration_term = exploration_weight * math.sqrt((2*log_total_visits) / child.visits)
            #print(exploitation_term + exploration_term)
            return exploitation_term + exploration_term

        # Choose the child with the maximum UCT value
        child_max = max(self.children, key=uct_value)
        if child_max.children:
            child_max = child_max.select_child()
        return child_max

    def expand(self):
        """Expand the node by adding a new child"""
        # create the child nodes of the current state based on the determinized game
        # update the cards played
        if not self.choices or self.depth >= self.max_depth:
            return self
        
        if self.unprocessed_choices:
            new_choice = self.unprocessed_choices.pop(0)
        else:
            return self

        new_hands = copy.deepcopy(self.hands)
        new_scores = copy.deepcopy(self.scores)
        next_player = copy.deepcopy(self.i)
        new_hand = []
        for card in self.hands[self.i]:
            if not card.equalTo(new_choice):
                new_hand.append(card)
        new_hands[self.i] = new_hand

        next_player +=1
        if next_player == self.players:
            next_player = 0
        cards_played = copy.deepcopy(self.cards_played)
        if len(cards_played) == self.players:
            for i, card1 in enumerate(cards_played):
                for card2 in cards_played:
                    if not card1.beats(card2, cards_played[0].getSuit(), self.trump):
                        break
                next_player = i
                new_scores[i] += 1
                
            cards_played = []
        cards_played.append(new_choice)
        child = GameTree(self, new_hands, cards_played, new_scores, self.bids, self.players, self.trump, next_player, self.initial_player, self.max_depth, self.depth + 1)
        self.children.append(child)
        return child

    def simulate(self):
        """Simulate a random playout from a expanded node"""
        # copy variables to send to random playout
        hands = copy.deepcopy(self.hands)
        scores = copy.deepcopy(self.scores)
        player = copy.deepcopy(self.i)
        cards_played = copy.deepcopy(self.cards_played)
        simulation_val = self.simulate_random_playout(hands, scores, player, cards_played)
        return simulation_val

    def simulate_random_playout(self, hands, scores, player, cards_played):
        """Simulation of random moves from the current cards"""
        while True: # until there are no more random moves to make, keep making random moves
            if len(cards_played) == self.players or not cards_played: # get player choices
                choices = hands[player]
                cards_played = []
            else:
                choices = self.get_choices(hands[player], self.cards_played[0])
            if not choices: # if no choices left then round is over
                return self.evaluate(scores) # return the evaluation of the final state
            if type(choices) is not list:
                choices = [choices]
            choice = random.choice(choices) # pick random choice
            hands[player] = [card for card in hands[player] if not card.equalTo(choice)] # remove choice from players hand
            cards_played.append(choice)
            player += 1
            if player == self.players:
                player = 0
            if len(cards_played) == self.players:
                for i, card1 in enumerate(cards_played):
                    # Assume player i has won until proven otherwise
                    player_wins = True        
                    for card2 in cards_played:
                        if card1.equalTo(card2):
                            continue
                        if not card1.beats(card2, cards_played[0].getSuit(), self.trump):
                            # Card1 does not beat card2, set player_wins to False and break the inner loop
                            player_wins = False
                            break
                    if player_wins:
                        # All comparisons passed, player i wins
                        player = (player + i) % 4
                        scores[player] += 1
                cards_played = []

    def evaluate(self, scores):
        if self.bids:
            if self.bids[self.i] == scores[self.i]:
                return scores[self.initial_player] + 10
            else:
                return scores[self.initial_player]
        else:
            return scores[self.initial_player]

        
    def backpropagate(self, result):
        """Update the wins and visits for this node and its ancestors"""
        current_node = self
        while current_node.parent:
            current_node.visits += 1
            current_node.wins += result
            current_node = current_node.parent
        return current_node

    def __str__(self, depth):
        """Returns the tree as a tree structure in depth-first order"""
        def hand_as_string(hand):
            hand_str = ""
            for card in hand:
                hand_str += card.__str__()
            return hand_str
        output = ""
        # Add spaces based on depth
        indentation = " " * (self.depth * 4)

        # Add symbols to represent the tree structure
        if self.parent:
            if self.parent.children[-1] == self:
                line_symbol = "└── "
            else:
                line_symbol = "├── "
            output += f"{indentation}{line_symbol}"
        output += f"depth={self.depth}, wins={self.wins}, visits={self.visits}, children = {len(self.children)}\n"
        # output += f"{indentation}├hand = {hand_as_string(self.hands[self.i])}\n"
        output += f"{indentation}├choices = {hand_as_string(self.choices)}\n"
        
        # for hand in self.other_players_hands:
        #     output += f"{indentation}├next_hand = {hand_as_string(hand)}\n"
        

        for child in self.children:
            if child.depth > depth:
                break
            output += child.__str__(depth)

        return output