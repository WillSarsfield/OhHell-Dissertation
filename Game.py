from Player import Player
import Round

#Game class that when called plays the number of rounds specified

class Game:
    def __init__(self, rounds) -> None:
        self.playerList = []
        for i in range(0,4):
            player = Player("player " + str(i+1))
            self.playerList.append(player)
        for i in range(0, rounds):
            Round.round(i % 4, i % 4, self.playerList)
    
    def getPlayers(self):#return player scores for statistics overview
        return self.playerList