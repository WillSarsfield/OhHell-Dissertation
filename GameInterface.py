import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Player import Player
from RealPlayer import RealPlayer
from InformedPlayer import InformedPlayer
from BestAgent import BestAgent
from Deck import Deck
from Hand import Hand
from Card import Card
import math
import time

class GameInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.players = 4
        self.hand_size = 13
        self.rounds = 4
        self.opponent_strengths = [1,1,1]
        self.title("Declaration Whist")
        self.geometry("650x650")
        self.resizable(False,False)
        self.bind("<Escape>", lambda event: self.destroy())
        # load background image
        self.background_image = tk.PhotoImage(file="Assets/grass.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # load card images 
        self.card_images =[]
        suitDict = {
            0: "hearts",
            1: "diamonds",
            2: "spades",
            3: "clubs"}
        for i in range(0, 4):
            card_list = []
            for j in range(1, 14):
                self.card_image = Image.open(f"Assets/card-{suitDict[i]}-{j}.png").resize((48,72))
                self.card_imagetk = ImageTk.PhotoImage(self.card_image)
                card_list.append(self.card_imagetk)
            self.card_images.append(card_list)
        self.new_game_button = tk.Button(self, text="New Game", font = ("Terminal", 24), command=self.new_game)
        self.new_game_button.place(x=200, y=300, relwidth=0.4, relheight=0.1)

    def new_game(self):
        self.new_game_button.destroy()
        # frame for game options
        self.options_title = tk.Label(self, text="Game Options", font = ("Terminal", 23), bd= 2, relief=tk.SUNKEN)
        self.options_title.place(x=170, y=240, relwidth=0.5, relheight=0.1)
        self.options_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.options_frame.place(x=170, y=300, relwidth=0.5, relheight=0.4)
        # option menu for number of players
        self.player_options = ["4", "3", "2"]
        self.selected_option_player = tk.StringVar(self)
        self.selected_option_player.set(self.player_options[0])
        self.player_menu_button = tk.Menubutton(self.options_frame, text=f"{self.players}", font = ("Terminal", 12), relief="raised")
        self.player_menu_button.grid(row=0, column = 1)
        self.player_options_menu = tk.Menu(self.player_menu_button, tearoff=False)
        for option in self.player_options:
            self.player_options_menu.add_command(label=option, command=lambda opt=option: self.on_player_select(opt))
        self.player_menu_button.configure(menu=self.player_options_menu)
        self.players_label = tk.Label(self.options_frame, text="Number of Players:", font = ("Terminal", 12))
        self.players_label.grid(row = 0, column = 0)
        # option menu for size of hands
        self.hand_size_options = ["13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
        self.selected_option_hand_size = tk.StringVar(self)
        self.selected_option_hand_size.set(self.hand_size_options[0])
        self.hand_size_menu_button = tk.Menubutton(self.options_frame, text=f"{self.hand_size}", font = ("Terminal", 12), relief="raised")
        self.hand_size_menu_button.grid(row = 1, column = 1)
        self.hand_size_options_menu = tk.Menu(self.hand_size_menu_button, tearoff=False)
        for option in self.hand_size_options:
            self.hand_size_options_menu.add_command(label=option, command=lambda opt=option: self.on_hand_size_select(opt))
        self.hand_size_menu_button.configure(menu=self.hand_size_options_menu)
        self.hand_size_label = tk.Label(self.options_frame, text="Size of Hand:", font = ("Terminal", 12))
        self.hand_size_label.grid(row = 1, column = 0)
        # option menu for number of rounds
        self.rounds_options = ["26", "13", "6", "5", "4", "3", "2", "1"]
        self.selected_option_rounds = tk.StringVar(self)
        self.selected_option_rounds.set(self.rounds_options[2])
        self.rounds_menu_button = tk.Menubutton(self.options_frame, text=f"{self.rounds}", font = ("Terminal", 12), relief="raised")
        self.rounds_menu_button.grid(row = 2, column = 1)
        self.rounds_options_menu = tk.Menu(self.rounds_menu_button, tearoff=False)
        for option in self.rounds_options:
            self.rounds_options_menu.add_command(label=option, command=lambda opt=option: self.on_rounds_select(opt))
        self.rounds_menu_button.configure(menu=self.rounds_options_menu)
        self.rounds_label = tk.Label(self.options_frame, text="Number of Rounds:", font = ("Terminal", 12))
        self.rounds_label.grid(row = 2, column = 0)
        # option menu for opponent's strength
        self.opponent_options = ["Easy", "Medium", "Hard"]
        self.selected_option_opponent = tk.StringVar(self)
        self.selected_option_opponent.set(self.opponent_options[1])
        self.opponent_menu_button = tk.Menubutton(self.options_frame, text=f"{self.selected_option_opponent.get()}", font = ("Terminal", 12), relief="raised")
        self.opponent_menu_button.grid(row = 3, column = 1)
        self.opponent_options_menu = tk.Menu(self.opponent_menu_button, tearoff=False)
        for option in self.opponent_options:
            self.opponent_options_menu.add_command(label=option, command=lambda opt=option: self.on_opponent_select(opt))
        self.opponent_menu_button.configure(menu=self.opponent_options_menu)
        self.opponent_label = tk.Label(self.options_frame, text="Opponent Strength:", font = ("Terminal", 12))
        self.opponent_label.grid(row = 3, column = 0)
        # start button
        self.start_button = tk.Button(self.options_frame, text="Start", font = ("Terminal", 20), command=self.start_game)
        self.start_button.grid(row = 4, column = 0)
    
    def on_player_select(self, value):
        self.players = int(value)
        self.player_menu_button.destroy()
        self.player_menu_button = tk.Menubutton(self.options_frame, text=f"{self.players}", font = ("Terminal", 12), relief="raised")
        self.player_menu_button.grid(row=0, column = 1)
        self.player_options_menu = tk.Menu(self.player_menu_button, tearoff=False)
        for option in self.player_options:
            self.player_options_menu.add_command(label=option, command=lambda opt=option: self.on_player_select(opt))
        self.player_menu_button.configure(menu=self.player_options_menu)
        difficulty = self.opponent_strengths[0]
        self.opponent_strengths = []
        for _ in range(self.players-1):
            self.opponent_strengths.append(difficulty)
    
    def on_hand_size_select(self, value):
        self.hand_size = int(value)
        self.hand_size_menu_button.destroy()
        self.hand_size_menu_button = tk.Menubutton(self.options_frame, text=f"{self.hand_size}", font = ("Terminal", 12), relief="raised")
        self.hand_size_menu_button.grid(row = 1, column = 1)
        self.hand_size_options_menu = tk.Menu(self.hand_size_menu_button, tearoff=False)
        for option in self.hand_size_options:
            self.hand_size_options_menu.add_command(label=option, command=lambda opt=option: self.on_hand_size_select(opt))
        self.hand_size_menu_button.configure(menu=self.hand_size_options_menu)

    def on_rounds_select(self, value):
        self.rounds = int(value)
        self.rounds_menu_button.destroy()
        self.rounds_menu_button = tk.Menubutton(self.options_frame, text=f"{self.rounds}", font = ("Terminal", 12), relief="raised")
        self.rounds_menu_button.grid(row = 2, column = 1)
        self.rounds_options_menu = tk.Menu(self.rounds_menu_button, tearoff=False)
        for option in self.rounds_options:
            self.rounds_options_menu.add_command(label=option, command=lambda opt=option: self.on_rounds_select(opt))
        self.rounds_menu_button.configure(menu=self.rounds_options_menu)

    def on_opponent_select(self, value):
        self.opponent_strengths = []
        if value == "Easy":
            for _ in range(self.players - 1):
                self.opponent_strengths.append(0)
        elif value == "Medium":
            for _ in range(self.players - 1):
                self.opponent_strengths.append(1)
        else:
            for _ in range(self.players - 1):
                self.opponent_strengths.append(2)
        self.opponent_menu_button.destroy()
        self.opponent_menu_button = tk.Menubutton(self.options_frame, text=f"{value}", font = ("Terminal", 12), relief="raised")
        self.opponent_options_menu = tk.Menu(self.opponent_menu_button, tearoff=False)
        for option in self.opponent_options:
            self.opponent_options_menu.add_command(label=option, command=lambda opt=option: self.on_opponent_select(opt))
        self.opponent_menu_button.configure(menu=self.opponent_options_menu)
        self.opponent_menu_button.grid(row = 3, column = 1)
    
    def start_game(self):
        self.options_title.destroy()
        self.options_frame.destroy()
        self.playerList = []
        optimisations =  [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
        self.real_player = RealPlayer("player 1")
        self.playerList.append(self.real_player)
        for i, difficulty in enumerate(self.opponent_strengths):
            if difficulty == 0:
                player = Player("player " + str(i+2))#make players with names
            elif difficulty == 1:
                player = InformedPlayer("player " + str(i+2), optimisations)#make informed players with names
            elif difficulty == 2:
                player = BestAgent(f"player {i+2}") #make best agents with names

            self.playerList.append(player)#add to list of players
        self.round_count = 1
        self.trump = 0
        self.hand_change = -1
        # initialise labels and frames
        # round label
        self.round_label = tk.Label(self, text=f"Round: {self.round_count}/{self.rounds}", font = ("Terminal", 20))
        self.round_label.place(x = 10, y = 20, relwidth=0.25, relheight=0.05)
        # trump label
        self.suitDict = { #translate suit value to symbol
            0: "♥",
            1: "♦",
            2: "♠",
            3: "♣"
        }
        self.trump_label = tk.Label(self, text=f"Trump: {self.suitDict[self.trump]}", font = ("Terminal", 20))
        self.trump_label.place(x = 180, y = 20, relwidth=0.2, relheight=0.05)
        # bid board
        self.bid_frame = tk.Frame(self)
        self.bid_frame.place(x = 320, y = 20, relwidth=0.22, relheight=0.2)
        self.bid_label = tk.Label(self.bid_frame, text = f"Bids: ", font = ("Terminal", 18))
        self.bid_label.grid(row=0,column=0)
        for i, player in enumerate(self.playerList):
            self.player_bid_label = tk.Label(self.bid_frame, text = f"{player.getName()}: {player.getBid()}", font = ("Terminal", 12))
            self.player_bid_label.grid(row = i+1, column = 0)
        # score board
        self.score_frame = tk.Frame(self)
        self.score_frame.place(x = 480, y = 20, relwidth=0.23, relheight=0.2)
        self.score_label = tk.Label(self.score_frame, text = f"Scores: ", font = ("Terminal", 18))
        self.score_label.grid(row=0,column=0)
        for i, player in enumerate(self.playerList):
            self.player_score_label = tk.Label(self.score_frame, text = f"{player.getScore()} + {player.getRoundScore()}", font = ("Terminal", 12))
            self.player_score_label.grid(row = i+1, column = 0)
        # playing table
        self.table_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.table_frame.place(x = 200, y = 175, relwidth=0.4, relheight=0.4)
        # winning card
        self.winner_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.winner_frame.place(x = 200, y = 365, relwidth=0.4, relheight=0.125)
        # hand
        self.hand_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.hand_frame.place(x = 110, y = 485, relwidth=0.7, relheight=0.25)
        self.play_round(0)
        
    def play_round(self, first):
        # initialise deck and deal cards
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.playerList:
            hand = Hand(self.deck.makeHand(self.hand_size))
            hand.sort()
            player.makeHand(hand)
            print(player)
        for i, card in enumerate(self.playerList[0].getHand().getCards()):
            self.show_card(self.hand_frame, card.getValue(), card.getSuit(), i, False)
        # get bid from player
        self.bidTotal = 0
        self.bids = []
        self.save_index = 0
        self.save_first = first
        for player in self.playerList:
            player.bid = 0
        for i in range(first , first + len(self.playerList)):
            self.playerList[i % len(self.playerList)].resetCardsInDeck()
            if i % len(self.playerList) == 0:
                self.save_index = i + 1
                self.get_bid()
                break
            if (i % len(self.playerList)) != len(self.playerList) - 1:
                if i == first:
                    self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, True, len(self.playerList), self.bids) #can make bid, argument passed represents a bid that is banned (14 passed as it is an unbiddable number)
                else:
                    self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                self.bidTotal += self.playerList[i % len(self.playerList)].getBid()
                print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                self.bids.append(self.playerList[i % len(self.playerList)].getBid())
            else:
                if self.bidTotal < self.hand_size + 1: #calculates the bid that is banned for the final player
                    self.playerList[i % len(self.playerList)].playBid(self.hand_size - self.bidTotal, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                else:
                    self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                self.bids.append(self.playerList[i % len(self.playerList)].getBid())
            self.update_bid_board()

    def get_bid(self):
        self.bid_options = []
        for i in range(self.hand_size + 1):
            self.bid_options.append(i)
        self.selected_option_bid = tk.StringVar(self)
        self.selected_option_bid.set(self.bid_options[0])
        self.bid_menu_button = tk.Menubutton(self.table_frame, text=f"{self.selected_option_bid.get()}", font = ("Terminal", 20), relief="raised")
        self.bid_menu_button.grid(row = 0, column = 1)
        self.bid_options_menu = tk.Menu(self.bid_menu_button, tearoff=False)
        for option in self.bid_options:
            self.bid_options_menu.add_command(label=option, command=lambda opt=option: self.on_bid_select(opt))
        self.bid_menu_button.configure(menu=self.bid_options_menu)
        self.new_bid_label = tk.Label(self.table_frame, text="Select Bid:", font = ("Terminal", 20))
        self.new_bid_label.grid(row = 0, column = 0)
        self.submit_button = tk.Button(self.table_frame, text="Start", font = ("Terminal", 18), command=self.submit_bid)
        self.submit_button.grid(row = 1, column = 0)

    def on_bid_select(self, value):
        self.playerList[0].playBid(value)
        self.bid_menu_button.destroy()
        self.bid_menu_button = tk.Menubutton(self.table_frame, text=f"{value}", font = ("Terminal", 20), relief="raised")
        self.bid_menu_button.grid(row = 0, column = 1)
        self.bid_options_menu = tk.Menu(self.bid_menu_button, tearoff=False)
        for option in self.bid_options:
            self.bid_options_menu.add_command(label=option, command=lambda opt=option: self.on_bid_select(opt))
        self.bid_menu_button.configure(menu=self.bid_options_menu)

    def submit_bid(self):
        print(f"player 1 bid: {self.playerList[0].getBid()}")
        self.bids.append(self.playerList[0].getBid())
        self.table_frame.destroy()
        self.table_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.table_frame.place(x = 200, y = 175, relwidth=0.4, relheight=0.4)
        if self.save_index <= self.save_first + len(self.playerList):
            for i in range(self.save_index , self.save_first + len(self.playerList)):
                if i % len(self.playerList) == 0:
                    self.save_index = i + 1
                    self.get_bid()
                    break
                if (i % len(self.playerList)) != len(self.playerList) - 1:
                    if i == self.save_first:
                        self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, True, len(self.playerList), self.bids) #can make bid, argument passed represents a bid that is banned (14 passed as it is an unbiddable number)
                    else:
                        self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                    self.bidTotal += self.playerList[i % len(self.playerList)].getBid()
                    print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                    self.bids.append(self.playerList[i % len(self.playerList)].getBid())
                else:
                    if self.bidTotal < self.hand_size + 1: #calculates the bid that is banned for the final player
                        self.playerList[i % len(self.playerList)].playBid(self.hand_size - self.bidTotal, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                    else:
                        self.playerList[i % len(self.playerList)].playBid(self.hand_size + 1, self.hand_size, self.trump, False, len(self.playerList), self.bids)
                    print("player " + str((i % len(self.playerList))+1) + " bid: " + str(self.playerList[i % len(self.playerList)].getBid()))
                    self.bids.append(self.playerList[i % len(self.playerList)].getBid())
                self.update_bid_board()
        self.update_bid_board()
        self.update_hand(-1, False)
        self.remaining_tricks = self.hand_size
        self.play_trick()

    def play_trick(self):
        if self.remaining_tricks == 0:
            self.winner_card = None
            self.winner_frame.destroy()
            self.cardList = [] #cardlist the trick will be passed into
            self.update_table()
            self.trump += 1
            self.trump = self.trump % 4
            self.update_trump()
            self.round_count += 1
            self.hand_size += self.hand_change
            if self.hand_size == 0:
                self.hand_change = 1
                self.hand_size = 2
            if self.hand_size > 13:
                self.hand_change = -1
                self.hand_size = 12
            if self.round_count > self.rounds:
                self.end()
                return
            self.update_round()
            self.play_round((self.round_count - 1) % self.players)
        else:
            self.winner_card = None
            self.remaining_tricks -= 1
            self.winner_frame.destroy()
            self.cardList = [] #cardlist the trick will be passed into
            self.update_table()
            self.scores = [0 for _ in range(len(self.playerList))]
            for j, player in enumerate(self.playerList):#save hand in history for display later
                self.scores[j] = player.getRoundScore()
            if self.save_first == 0:
                print("first = " + str(self.save_first + 1))
                print("player " + str(self.save_first + 1) + "'s turn:")
                self.update_hand(-1, True)
                self.save_index = 1
                return
            print("first = " + str(self.save_first + 1))
            options = self.playerList[self.save_first].getOptions() #lead player collects all the possible plays it can make
            print("player " + str(self.save_first + 1) + "'s turn:")
            self.leadCard = self.playerList[self.save_first].playOption(options, self.cardList, self.trump, len(self.playerList), self.bids, self.scores) #lead player chooses a play from its options
            print(self.leadCard)
            self.cardList.append(self.leadCard) #lead card is added to the trick
            self.update_table()
            for i in range(self.save_first + 1 , self.save_first + len(self.playerList)): #iterate over remaining players choices in order ascending from first player
                if i % self.players == 0:
                    self.update_hand(self.leadCard.getSuit(), True)
                    self.save_index = i + 1
                    return
                options = self.playerList[i % len(self.playerList)].getOptions(self.leadCard.getSuit()) #player collects all the possible plays it can make
                print("player " + str((i % len(self.playerList)) + 1) + "'s turn:")
                card = self.playerList[i % len(self.playerList)].playOption(options, self.cardList, self.trump, len(self.playerList), self.bids, self.scores) #player chooses a play from its options
                print(card)
                self.cardList.append(card) #card played added to list
                self.update_table()
            for player in self.playerList:
                player.updateCardsInDeck(self.cardList)

    def show_card(self, frame, card_val, card_suit, i, option):
        current_card = Card(card_val, card_suit)
        if card_val == 14:
            card_val = 1
        if option:
            card = ttk.Button(frame, image=self.card_images[card_suit][card_val-1], command=lambda: self.play_card(current_card))
        else:
            card = ttk.Label(frame, image=self.card_images[card_suit][card_val-1])
        if i < 7:
            card.grid(row = 0, column = i)
        else:
            card.grid(row = 1, column = i - 7)

    def play_card(self, card):
        print(card)
        self.playerList[0].playOption(card)
        self.update_hand(-1, False)
        if not self.cardList:
            self.leadCard = card
        if self.save_index % self.players == 1:
            self.cardList.append(card)
            self.update_table()
            for i in range(self.save_index , self.save_first + len(self.playerList)): #iterate over remaining players choices in order ascending from first player
                if i % self.players == 0:
                    self.save_index = i + 1
                    return
                options = self.playerList[i % len(self.playerList)].getOptions(self.leadCard.getSuit()) #player collects all the possible plays it can make
                print("player " + str((i % len(self.playerList)) + 1) + "'s turn:")
                card = self.playerList[i % len(self.playerList)].playOption(options, self.cardList, self.trump, len(self.playerList), self.bids, self.scores) #player chooses a play from its options
                print(card)
                self.cardList.append(card) #card played added to list
                self.update_table()
                for player in self.playerList:
                    player.updateCardsInDeck(self.cardList)
            self.save_first = self.trick()
            self.playerList[self.save_first].addRoundScore(1) #update winning player's score
            if self.remaining_tricks == 0:
                for player in self.playerList: #awards bonus points to any player who matched their bid at the end of the round
                    if player.getRoundScore() == player.getBid():
                        player.addRoundScore(10)
                        player.addScore(player.getRoundScore())
                        player.updateBidsMade()
                    else:
                        player.addScore(player.getRoundScore())
                    player.roundScore = 0
            self.update_winner_frame()
            self.update_score_board()


    # find winner from trick to set to the new first, update scores, update displays, make an okay button on the winner frame
    
    def trick(self):
        winner = self.save_first #winner is set as the first player to start
        self.winner_card = self.cardList[0]
        leadSuit = self.winner_card.getSuit()
        i = 0 #count needed to format player turns correctly
        for card in self.cardList:
            if card.beats(self.winner_card, leadSuit, self.trump):
                winner = (self.save_first + i) % self.players #set winner to current index of card played
                self.winner_card = card   
            i += 1
        print("Card that won:")
        print(self.winner_card)
        return winner #return the index of the player that won
    
    def update_round(self): # update round the game is on out of total rounds
        self.round_label.destroy()
        self.round_label = tk.Label(self, text=f"Round: {self.round_count}/{self.rounds}", font = ("Terminal", 20))
        self.round_label.place(x = 10, y = 20, relwidth=0.25, relheight=0.05)

    def update_trump(self): # update trump suit for that round
        self.trump_label.destroy()
        self.trump_label = tk.Label(self, text=f"Trump: {self.suitDict[self.trump]}", font = ("Terminal", 20))
        self.trump_label.place(x = 180, y = 20, relwidth=0.2, relheight=0.05)

    def update_score_board(self): # update score board frame
        self.score_frame.destroy()
        self.score_frame = tk.Frame(self)
        self.score_frame.place(x = 480, y = 20, relwidth=0.23, relheight=0.2)
        self.score_label = tk.Label(self.score_frame, text = f"Scores: ", font = ("Terminal", 18))
        self.score_label.grid(row=0,column=0)
        for i, player in enumerate(self.playerList):
            self.player_score_label = tk.Label(self.score_frame, text = f"{player.getScore()} + {player.getRoundScore()}", font = ("Terminal", 12))
            self.player_score_label.grid(row = i+1, column = 0)

    def update_bid_board(self): # update bid board frame
        self.bid_frame.destroy()
        self.bid_frame = tk.Frame(self)
        self.bid_frame.place(x = 320, y = 20, relwidth=0.22, relheight=0.2)
        self.bid_label = tk.Label(self.bid_frame, text = f"Bids: ", font = ("Terminal", 18))
        self.bid_label.grid(row=0,column=0)
        for i, player in enumerate(self.playerList):
            self.player_bid_label = tk.Label(self.bid_frame, text = f"{player.getName()}: {player.getBid()}", font = ("Terminal", 12))
            self.player_bid_label.grid(row = i+1, column = 0)
    
    def update_table(self): # update the cards on the table
        self.table_frame.destroy()
        self.table_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.table_frame.place(x = 200, y = 175, relwidth=0.4, relheight=0.4)
        for i, card in enumerate(self.cardList):
            self.show_card(self.table_frame, card.getValue(), card.getSuit(), i, False)

    def update_winner_frame(self): # update the frame showing who won the trick
        self.winner_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.winner_frame.place(x = 200, y = 365, relwidth=0.4, relheight=0.125)
        self.winner_label = tk.Label(self.winner_frame, text = f"Winner: player {self.save_first + 1}", font = ("Terminal", 12))
        self.winner_label.grid(row = 0, column = 0)
        self.show_card(self.winner_frame, self.winner_card.getValue(), self.winner_card.getSuit(), 7, False)
        self.winner_button = tk.Button(self.winner_frame, text = "OK", font = ("Terminal", 12), command=self.play_trick)
        self.winner_button.grid(row = 1, column = 1)


    def update_hand(self, lead, choose): # update cards in player's hand
        self.hand_frame.destroy()
        self.hand_frame = tk.Frame(self, bd= 2, relief=tk.SUNKEN)
        self.hand_frame.place(x = 110, y = 485, relwidth=0.7, relheight=0.25)
        card_options = Deck()
        card_options.cardList = self.playerList[0].getOptions(lead)
        for i, card in enumerate(self.playerList[0].getHand().getCards()):
            if card_options.contains(card) and choose:     
                self.show_card(self.hand_frame, card.getValue(), card.getSuit(), i, True)
            else:
                self.show_card(self.hand_frame, card.getValue(), card.getSuit(), i, False)
    
    def end(self):
        self.score_frame.destroy()
        self.hand_frame.destroy()
        self.bid_frame.destroy()
        self.trump_label.destroy()
        self.score_frame = tk.Frame(self)
        self.score_frame.place(x = 200, y = 175, relwidth=0.4, relheight=0.4)
        self.score_label = tk.Label(self.score_frame, text = f"Final Scores: ", font = ("Terminal", 20))
        self.score_label.grid(row=0,column=0)
        for i, player in enumerate(self.playerList):
            self.player_score_label = tk.Label(self.score_frame, text = f"player {i + 1}: {player.getScore()}", font = ("Terminal", 20))
            self.player_score_label.grid(row = i+1, column = 0)


if __name__ == "__main__":
    game = GameInterface()
    game.mainloop()
