import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Game import Game
import math
import time

class PlayerWindow(tk.Tk):
    def __init__(self, playerList, player, cardsPlayed, winningCards, currentLead, currentBids):
        super().__init__()
        self.playerList = playerList
        self.player = player
        self.cardsPlayed = cardsPlayed
        self.winningCards = winningCards
        self.currentLead = currentLead
        self.currentBids = currentBids
        self.title("Declaration Whist")
        self.geometry("650x650")
        self.resizable(False,False)
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind('<Return>', self.on_key_press)
        self.frame = 0
        self.round = 1
        self.roundFrame = self.round

        self.background_image = tk.PhotoImage(file="Assets/grass.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.player_label = tk.Label(self, text = self.player.getName(), font = ("Terminal", 24))
        self.player_label.grid(row=0,column=0)
        self.score_label = tk.Label(self, text = f"Score: {self.player.getScoreHistory()[self.frame]}", font = ("Terminal", 16))
        self.score_label.grid(row=0, column=1)
        self.lead_label = tk.Label(self, text = "", font = ("Terminal", 16))
        self.bids_frame = tk.Frame(self)

        self.hand = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.hand.place(x=120, y=500, relwidth=0.645, relheight=0.3)

        self.playZone = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.playZone.place(x=192, y=162, relwidth=0.4, relheight=0.4)


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
        if i > 7:
            card.grid(row = 1, column = i - 8)
        elif i > 99:
            card.grid(row = 1, column = 2)
        else: 
            card.grid(row = 0, column = i)

    def check_key_press(self):
        if self.key_pressed:
            print(f'You pressed {self.key_pressed}')
            self.quit()
        else:
            self.after(100, self.check_key_press)

    def on_key_press(self, event):
        self.frame += 1
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
        j = 100
        if self.winningCards[self.frame] != None:
            self.show_card(self.playZone,  self.winningCards[self.frame].getValue(), self.winningCards[self.frame].getSuit(), j, self.card_images)
        self.score_label.destroy()
        self.score_label = tk.Label(self, text = f"Score: {self.player.getScoreHistory()[self.frame]}", font = ("Terminal", 16))
        self.score_label.grid(row=0, column=1)
        self.lead_label.destroy()
        self.lead_label = tk.Label(self, text = f"Lead: {self.playerList[self.currentLead[self.frame]].getName()}", font = ("Terminal", 16))
        self.lead_label.grid(row=0,column=2)
        if not self.player.getHandHistory()[self.frame]:
            self.round += 1
            self.roundFrame = self.frame
        self.bids_frame.destroy()
        self.bids_frame = tk.Frame(self)
        self.bids_frame.grid(row=1, column=0)
        self.bids_label = tk.Label(self.bids_frame, text = f"Bids: ", font = ("Terminal", 16))
        self.bids_label.grid(row=1,column=0)
        for i in range(self.currentLead[self.roundFrame], self.currentLead[self.roundFrame] + len(self.playerList)):
            self.bids_label = tk.Label(self.bids_frame, text = f"{self.playerList[i % len(self.playerList)].getName()} :  {str(self.currentBids[self.round][i % len(self.playerList)])}", font = ("Terminal", 16))
            self.bids_label.grid(row= i + 2,column=0)

        

if __name__ == "__main__":
    rounds = 13
    players = 4
    startTime = time.time()
    game = Game(rounds, players)
    playerList = game.getPlayers()
    player = game.getPlayers()[0]
    cardsPlayed = game.getCardsPlayed()
    winningCards = game.getWinningCards()
    currentLead = game.getCurrentLead()
    currentBids = game.getCurrentBids()
    print(currentBids)
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    window = PlayerWindow(playerList, player, cardsPlayed, winningCards, currentLead, currentBids)
    window.mainloop()
