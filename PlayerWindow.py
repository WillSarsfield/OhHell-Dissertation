import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Game import Game
import math
import time

class PlayerWindow(tk.Tk):
    def __init__(self, playerList, player, cardsPlayed, winningCards, currentLead, currentBids, trumps):
        super().__init__()
        self.playerList = playerList
        self.player = player
        self.cardsPlayed = cardsPlayed
        self.winningCards = winningCards
        self.currentLead = currentLead
        self.currentBids = currentBids
        self.trumps = trumps
        self.title("Declaration Whist")
        self.geometry("650x650")
        self.resizable(False,False)
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind('<Return>', self.on_key_press)
        self.frame = 0
        self.round = 0
        self.roundFrame = self.round

        self.background_image = tk.PhotoImage(file="Assets/grass.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.player_label = tk.Label(self, text = self.player.getName(), font = ("Terminal", 24))
        self.player_label.grid(row=0,column=0, padx=10, pady=10)
        self.score_label = tk.Label(self, text = f"Score: {self.player.getScoreHistory()[self.frame]}", font = ("Terminal", 16))
        self.score_label.grid(row=0, column=1, padx=10, pady=10)
        self.trump_label = tk.Label(self)
        self.lead_label = tk.Label(self)
        self.bids_frame = tk.Frame(self)
        self.round_label = tk.Label(self)

        self.hand = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.hand.place(x=120, y=500, relwidth=0.645, relheight=0.3)

        self.playZone = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.playZone.place(x=192, y=162, relwidth=0.4, relheight=0.4)

        self.winZone = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.winZone.place(x=192, y=360, relwidth=0.4, relheight=0.12)
        self.winner_label = tk.Label(self.winZone)

        suitDict = {
            0: "hearts",
            1: "diamonds",
            2: "spades",
            3: "clubs"}
        self.card_images =[]
        for i in range(0,52):
            suit = math.floor(i/13)
            value = ((i+1) %13) + 1
            #print(f"Assets/card-{suitDict[suit]}-{value}.png")
            self.card_image = Image.open(f"Assets/card-{suitDict[suit]}-{value}.png").resize((48,72))
            self.card_imagetk = ImageTk.PhotoImage(self.card_image)
            self.card_images.append(self.card_imagetk)
        i=0
        for card in self.player.getHandHistory()[self.frame]:
            self.show_card(self.hand, card.getValue(), card.getSuit(), i,self.card_images)
            i+=1

    def show_card(self, frame, value, suit, i, card_images):
        x = value - 2 + (13 * suit)
        card = ttk.Label(frame, image = card_images[x])       
        if frame == self.playZone:
            if i > 4:
                card.grid(row = 1, column = i - 5)
            else: 
                card.grid(row = 0, column = i)
        else:
            if i > 7:
                card.grid(row = 1, column = i - 8)
            else: 
                card.grid(row = 0, column = i)
        

    def on_key_press(self, event):
        self.frame += 1
        if len(self.player.getHandHistory()) <= self.frame:
            self.score_label.destroy()
            self.score_label = tk.Label(self, text = f"Score: {self.player.getScoreHistory()[-1]}", font = ("Terminal", 16))
            self.score_label.grid(row=0, column=1, padx=10, pady=10)
            self.bids_frame.destroy()
            self.bids_frame = tk.Frame(self)
            self.bids_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            self.bids_label = tk.Label(self.bids_frame, text = f"Scores: ", font = ("Terminal", 16))
            self.bids_label.grid(row=1,column=0)
            i = 0
            for p in self.playerList:
                self.bids_label = tk.Label(self.bids_frame, text = f"{p.getName()} :  {str(p.getScore())}", font = ("Terminal", 16))
                self.bids_label.grid(row= i + 2,column=0)
                i += 1
            return
        print(f"frame: {self.frame}")
        self.hand.destroy()
        self.hand = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.hand.place(x=120, y=500, relwidth=0.645, relheight=0.3)
        i = 0
        for card in self.player.getHandHistory()[self.frame]:
            self.show_card(self.hand, card.getValue(), card.getSuit(), i,self.card_images)
            i+=1
        self.playZone.destroy()
        self.playZone = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.playZone.place(x=192, y=162, relwidth=0.4, relheight=0.4)
        j = 0
        for card in self.cardsPlayed[self.frame]:
            self.show_card(self.playZone, card.getValue(), card.getSuit(), j, self.card_images)
            j+=1
        j = 1
        self.winZone.destroy()
        self.winZone = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.winZone.place(x=192, y=360, relwidth=0.4, relheight=0.12)
        x = 0
        winner = currentLead[self.frame-1]
        for card in self.cardsPlayed[self.frame]:
            if card.getValue() == self.winningCards[self.frame].getValue() and card.getSuit() == self.winningCards[self.frame].getSuit():
                winner = currentLead[self.frame-1] + x
                break
            x += 1
        winning_player = self.playerList[winner % len(self.playerList)]
        self.winner_label = tk.Label(self.winZone, text = f"Winner: {winning_player.getName()}", font = ("Terminal", 16))
        self.winner_label.grid(row=0, column=0)
        if self.winningCards[self.frame] != None:
            self.show_card(self.winZone,  self.winningCards[self.frame].getValue(), self.winningCards[self.frame].getSuit(), j, self.card_images)
        self.score_label.destroy()
        self.score_label = tk.Label(self, text = f"Score: {self.player.getScoreHistory()[self.frame]}", font = ("Terminal", 16))
        self.score_label.grid(row=0, column=1, padx=10, pady=10)
        self.lead_label.destroy()
        self.lead_label = tk.Label(self, text = f"Lead: {self.playerList[self.currentLead[self.frame-1]].getName()}", font = ("Terminal", 16))
        self.lead_label.grid(row=0,column=2, padx=10, pady=10)
        self.bids_frame.destroy()
        self.bids_frame = tk.Frame(self)
        self.bids_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.bids_label = tk.Label(self.bids_frame, text = f"Bids: ", font = ("Terminal", 16))
        self.bids_label.grid(row=1,column=0)
        for i in range(self.currentLead[self.roundFrame], self.currentLead[self.roundFrame] + len(self.playerList)):
            self.bids_label = tk.Label(self.bids_frame, text = f"{self.playerList[i % len(self.playerList)].getName()} :  {str(self.currentBids[self.round][i % len(self.playerList)])}", font = ("Terminal", 16))
            self.bids_label.grid(row= i + 2,column=0)
        suitDict = {
        0: "hearts",
        1: "diamonds",
        2: "spades",
        3: "clubs"}
        self.trump_label.destroy()
        self.trump_label = tk.Label(self, text = f"Trump: {suitDict[self.trumps[self.round]]}", font = ("Terminal", 16))
        self.trump_label.grid(row=0, column=3, padx=10, pady=10)
        self.round_label.destroy()
        self.round_label = tk.Label(self, text = f"Round: {self.round+1}",  font = ("Terminal", 16))
        self.round_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        if not self.player.getHandHistory()[self.frame]:
            self.round += 1
            self.roundFrame = self.frame + 1
        

if __name__ == "__main__":
    rounds = 2
    players = 4
    playerStrengths = [1,1,1,1]
    startTime = time.time()
    game = Game(rounds, players, playerStrengths, True)
    playerList = game.getPlayers()
    player = game.getPlayers()[0]
    cardsPlayed = game.getCardsPlayed()
    winningCards = game.getWinningCards()
    currentLead = game.getCurrentLead()
    currentBids = game.getCurrentBids()
    trumps = game.getTrumps()
    for hand in player.getHandHistory():
        for card in hand:
            print(card, end=" ")
        print()
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    window = PlayerWindow(playerList, player, cardsPlayed, winningCards, currentLead, currentBids, trumps)
    window.mainloop()
