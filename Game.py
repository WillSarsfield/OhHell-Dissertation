from Player import Player
import Round

#Game class that when called plays the number of rounds specified

class Game:
    def __init__(self, rounds) -> None:
        self.players = 4 #number of players
        self.playerList = []
        for i in range(0, self.players):
            player = Player("player " + str(i+1))#make players with names
            self.playerList.append(player)#add to list of players
        for i in range(0, rounds):#run round function rounds times
            Round.round(i % 4, i % 4, self.playerList)#change the player going first and the trump each time = {0,...,3}
    
    def getPlayers(self):#return player scores for statistics overview
        return self.playerList