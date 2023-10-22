from Player import Player
from Round import Round

class Game:
    def __init__(self) -> None:
        playerList = []
        for i in range(0,4):
            player = Player("player " + str(i+1))
            playerList.append(player)
        for i in range(0,4):
            round = Round(i, i, playerList)
        for player in playerList:
            print(player)
            print(player.getScore())