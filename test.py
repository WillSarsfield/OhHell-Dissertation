from Game import Game
import time
import numpy as np
rounds = 13
players = 4
startTime = time.time()
game = Game(rounds, players)
print("---%s seconds---" % (time.time() - startTime))
print("Rounds played: " + str(rounds))
for player in game.getPlayers():
    print(player)
    print(player.getScore())