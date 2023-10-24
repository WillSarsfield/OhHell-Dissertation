from Game import Game
import time
rounds = 5
players = 5
startTime = time.time()
game = Game(rounds, players)
print("---%s seconds---" % (time.time() - startTime))
print("Rounds played: " + str(rounds))
for player in game.getPlayers():
    print(player)
    print(player.getScore())