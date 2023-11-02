import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math
import time
import random

class MenuScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Menu")
        self.label.grid()
        self.play_button = tk.Button(self, text = "New Game", command=self.new_game)
        self.play_button.grid()
        self.exit_button = tk.Button(self, text = "Quit", command=self.quit)
        self.exit_button.grid()

    def new_game(self):
        self.master.switch_frame(GameScreen)

class GameScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(width=960, height=540)
        self.display_game()

    def display_game(self):
        self.label = tk.Label(self, text="Play Game")
        self.label.grid(row=0,column=0)
        self.switch_button = tk.Button(self, text="Menu", command=self.menu)
        self.switch_button.grid(row=0,column=1)
        self.card_grid = CardGrid(master = self)
        self.card_grid.config(width=960, height=540)
        self.card_grid.grid(row=1,column=0,sticky="s")
        #self.grid_rowconfigure((1))

    def menu(self):
        self.master.switch_frame(MenuScreen)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Declaration Whist")
        self.geometry("960x540")
        self.resizable(False,False)
        # self.bind("<F11>", lambda event: self.attributes("-fullscreen", True))
        # self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.current_frame = None
        self.switch_frame(MenuScreen)
        self.background_image = Image.open("Assets/grass.png")
        self.background_imagetk = ImageTk.PhotoImage(self.background_image)
        self.background = ttk.Label(self, image = self.background_imagetk)
        self.background.grid(row = 0, column = 0)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.grid(row=0,column=0)


class CardGrid(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.background='#323232'
        self.master = master
        #self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12))
        #self.grid_rowconfigure((0))
        suitDict = {
            0: "hearts",
            1: "diamonds",
            2: "spades",
            3: "clubs"
        }
        self.card_images =[]
        for i in range(0,52):
            suit = math.floor(i/13)
            value = ((i+1) %13) + 1
            #print(f"Assets/card-{suitDict[suit]}-{value}.png")
            self.card_image = Image.open(f"Assets/card-{suitDict[suit]}-{value}.png").resize((48,72))
            self.card_imagetk = ImageTk.PhotoImage(self.card_image)
            self.card_images.append(self.card_imagetk)
        for i in range(0,13):
            self.show_card(random.randint(2,14), random.randint(0,3), i)

    def show_card(self, value, suit, i):
        x = value - 2 + (13 * suit)
        self.card = ttk.Label(self, image = self.card_images[x])
        self.card.grid(row = 0, column = i,sticky="s")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
