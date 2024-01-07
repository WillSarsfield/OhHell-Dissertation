import random
import math
import time
import numpy as np
import copy
from collections import defaultdict

class GameTree:

    def __init__(self, parent = None, hand = None, other_players_hands = [], cards_played = [], score = 0, bids = None, players = None, max_depth = None, depth = 0) -> None:
        self.parent = parent
        self.children = []
        self.hand = hand # cards player has 
        self.other_players_hands = other_players_hands # cards other players have
        self.cards_played = cards_played # cards that have been played in the trick
        self.score = score # current score
        self.bids = bids
        self.players = players # number of players
        self.max_depth = max_depth
        self.depth = depth
        self.visits = 0 # times node was visited
        self.wins = 0 # times node made bid
        self.choices = []
        if len(cards_played) == players or not cards_played:
            self.choices = self.hand
        else:
            self.choices = self.get_choices(self.cards_played[0])
        if self.depth >= self.max_depth or not self.choices: # if depth is exceeded or player has no moves (round finished) then return
            return

    def get_choices(self, leadCard):
        choices = []
        for card in self.hand: #add cards of the same suit as the lead to the options
            if card.getSuit() == leadCard.getSuit():
                choices.append(card)
        if not choices: #if no cards with the same suit as the lead, all cards are options
            choices = self.hand
        return choices

    def determinize(self, unseen):
        # already played a card in trick so must deduct cards from initial players hands
        indent = 0
        if self.cards_played:
            indent = len(self.cards_played)
        # select random distribution of unseen cards for other players to have
        for _ in range(self.players - 1):
            if indent > 0:
                random_hand = random.sample(unseen.getCards(), k=len(self.hand) - 1)
            else:
                random_hand = random.sample(unseen.getCards(), k=len(self.hand))
                for card in random_hand:
                    print(card, end = " ")
                print()
            indent -= 1
            self.other_players_hands.append(random_hand)
            # remove selected cards from unseen
            for card in random_hand:
                unseen.removeCard(card)
    
    def select_choice(self):
        best_child = max(self.children, key=lambda child: child.wins)
        best_children = [child for child in self.children if child.wins == best_child.wins]
        best_child = random.choice(best_children)

        # find the difference between the cards
        differing_position = tuple(np.argwhere(self.board != best_child.board)[0])

        return differing_position


    def select_child(self, exploration_weight=1.4):
        """Select a child node using UCT (Upper Confidence Bound for Trees) formula"""
        # if no children, select itself
        if not self.children:
            return self
        if self.visits:
            log_total_visits = math.log(self.visits)
        # if all choices do not have a node, select itself
        if len(self.children) < len(self.choices):
            return self

        def uct_value(child):
            return 1
            exploitation_term = child.wins / child.visits
            exploration_term = exploration_weight * math.sqrt((2*log_total_visits) / child.visits)
            #print(exploitation_term + exploration_term)
            return exploitation_term + exploration_term

        # Choose the child with the maximum UCT value
        child_max = max(self.children, key=uct_value)

        return child_max

    def expand(self):
        """Expand the node by adding a new child"""
        # create the child nodes of the current state based on the determinized game
        # update the cards played
        if not self.choices:
            return self
        new_choice = None

        if self.children:
            for choice in self.choices:
                premade = False
                for child in self.children:
                    if child.cards_played[-1].equalTo(choice):
                        premade = True
                    
                if not premade:
                    new_choice = choice
                if new_choice:
                    break
        else:
            new_choice = self.choices[0]

        next_player_hand = []
        other_players_hands = copy.deepcopy(self.other_players_hands)
        new_bids = copy.deepcopy(self.bids)
        new_hand = []
        for card in self.hand:
            if not card.equalTo(new_choice):
                new_hand.append(card)

        # update the next player's hand and that player's opponent hands
        for i, hand in enumerate(self.other_players_hands):
            if len(hand) == len(self.hand):
                next_player_hand = hand
                temp = new_bids[0]
                new_bids[0] = new_bids[i + 1]
                new_bids[i + 1] = temp
                other_players_hands[i] = new_hand
                break
        cards_played = copy.deepcopy(self.cards_played)
        if len(cards_played) == 4:
            cards_played = []

        cards_played.append(new_choice)
        child = GameTree(self, next_player_hand, other_players_hands, cards_played, self.score, new_bids, self.players, self.max_depth, self.depth + 1)
        self.children.append(child)
        return child

    def simulate(self):
        """Simulate a random playout from a expanded node"""
        # copy variables to send to random playout

        #
        simulation_val = self.simulate_random_playout()
        return simulation_val

    def simulate_random_playout(self, hand, unseen):
        """Simulation of random moves from the current cards"""
        pass
        while True: # until there are no more random moves to make, keep making random moves
            pass
        return self.evaluate(board) # return the evaluation of the final state

    def evaluate(self, score):
        pass
        
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
        output += f"{indentation}├hand = {hand_as_string(self.hand)}\n"
        output += f"{indentation}├choices = {hand_as_string(self.choices)}\n"
        
        # for hand in self.other_players_hands:
        #     output += f"{indentation}├next_hand = {hand_as_string(hand)}\n"
        

        for child in self.children:
            if child.depth > depth:
                break
            output += child.__str__(depth)

        return output