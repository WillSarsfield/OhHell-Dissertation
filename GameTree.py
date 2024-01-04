import random
import math
import time
import numpy as np
import copy
from collections import defaultdict

class GameTree:

    def __init__(self, parent = None, hand = None, other_players_hands = [], cards_played = None, score = 0, players = None, max_depth = None, depth = 0) -> None:
        self.parent = parent
        self.children = []
        self.hand = hand # cards player has 
        self.other_players_hands = other_players_hands # cards other players have
        self.cards_played = cards_played # cards that have been played in the trick
        self.score = score # current score
        self.players = players # number of players
        self.max_depth = max_depth
        self.depth = depth
        self.visits = 0 # times node was visited
        self.wins = 0 # times node made bid
        self.choices = []
        if not cards_played:
            self.choices = self.hand
        else:
            self.choices = self.get_choices(self.cards_played[0])
        if self.depth >= self.max_depth or not self.choices: # if depth is exceeded or player has no moves (round finished) then return
            return

    def get_choices(self, leadCard):
        choices = []
        for card in self.hand.getCards(): #add cards of the same suit as the lead to the options
            if card.getSuit() == leadCard.getSuit():
                choices.append(card)
        if not choices: #if no cards with the same suit as the lead, all cards are options
            choices = self.hand.getCards()
        return choices

    def determinize(self, unseen):
        # already played a card in trick so must deduct cards from initial players hands
        indent = len(self.cards_played)
        # select random distribution of unseen cards for other players to have
        for _ in range(self.players):
            if indent > 0:
                random_hand = random.sample(unseen.getCards(), k=len(self.hand_size - 1))
            else:
                random_hand = random.sample(unseen.getCards(), k=len(self.hand_size))
            indent -= 1
            self.other_players_hands.append(random_hand)
            # remove selected cards from unseen
            for card in random_hand:
                unseen.removeCard(card)
        # create the child nodes of the current state based on the determinized game
        next_player_hand = []
        other_players_hands = copy.deepcopy(self.other_players_hands)
        end = True
        # update the next player's hand and that players opponent hands
        for i, hand in enumerate(self.other_players_hands):
            if len(hand) == len(self.hand):
                next_player_hand = hand
                other_players_hands[i] = self.hand
                end = False
                break
        # update the cards played
        cards_played = copy.deepcopy(self.cards_played)
        for choice in self.choices:
            if end:
                cards_played = []
            else:
                cards_played.append(choice)
            child = GameTree(self, next_player_hand, other_players_hands, cards_played)
    
    def select_choice(self):
        best_child = max(self.children, key=lambda child: child.wins)
        best_children = [child for child in self.children if child.wins == best_child.wins]
        best_child = random.choice(best_children)

        # find the difference between the cards
        differing_position = tuple(np.argwhere(self.board != best_child.board)[0])

        return differing_position


    def select_child(self, exploration_weight=1.4):
        """Select a child node using UCT (Upper Confidence Bound for Trees) formula"""
        if not self.children:
            return self

        if self.visits == 0:
            # No visits yet, randomly select a child
            return random.choice(self.children)

        log_total_visits = math.log(self.visits)

        for child in self.children:
            if child.visits == 0:
                return child

        def uct_value(child):
            exploitation_term = child.wins / child.visits
            exploration_term = exploration_weight * math.sqrt((2*log_total_visits) / child.visits)
            #print(exploitation_term + exploration_term)
            return exploitation_term + exploration_term

        # Choose the child with the maximum UCT value
        child_max = max(self.children, key=uct_value)

        return child_max

    def expand(self):
        """Expand the node by adding a new child"""
        if self.choices:
            choice = random.choice(self.choices)
            new_board = np.copy(self.board)
            new_board[choice[0], choice[1]] = self.colour
            new_choices = list(zip(*np.where(new_board == 0)))
            child = GameTree(self, new_board, new_choices, self.opp_colour(self.colour), self.root_colour, self.max_depth, self.depth + 1, self.width, self.board_size, self.time_start)  
            self.children.append(child)
            return child
        if not self.choices:
            return self
        return None

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
        return self.evaluate(board) # return the evaluation of the final board with no choices left

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

        for child in self.children:
            if child.depth > depth:
                break
            output += child.__str__(depth)

        return output