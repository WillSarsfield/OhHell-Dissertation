from Game import Game
import time
rounds = 13
startTime = time.time()
game = Game(rounds)
print("---%s seconds---" % (time.time() - startTime))
print("Rounds played: " + str(rounds))
for player in game.getPlayers():
    print(player)
    print(player.getScore())