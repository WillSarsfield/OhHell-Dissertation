import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math
import time
import random

class PlayerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Declaration Whist")
        self.geometry("650x650")
        self.resizable(False,False)
        self.background_image = tk.PhotoImage(file="Assets/grass.png")

        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
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
        for i in range(0,13):
            self.show_card(self.hand, random.randint(2,14), random.randint(0,3), i, self.card_images)

    def show_card(self, frame, value, suit, i, card_images):
        x = value - 2 + (13 * suit)
        card = ttk.Label(frame, image = card_images[x])
        if i > 7:
            card.grid(row = 1, column = i - 8)
        else: 
            card.grid(row = 0, column = i)

if __name__ == "__main__":
    app = PlayerWindow()
    app.mainloop()