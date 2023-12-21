from Game import Game
import time
import sys, os
import numpy as np
import matplotlib as plt

informedPlayerScores = []
randomPlayerScores = []
rounds = 2
players = 4
playerStrengths1 = [1,1,1,1]
verbose = True
samples = 1
startTime = time.time()
for i in range(0, samples):
    game = Game(rounds, players, playerStrengths1, verbose)
    informedPlayerScores.append(game.getPlayers()[0].getScore())
sys.stdout = sys.__stdout__
print("---%s seconds---" % (time.time() - startTime))
print("Rounds played: " + str(rounds))
informednp = np.array(informedPlayerScores)
print("informed mean: " + str(np.mean(informednp)))
print("informed standard deviation: " + str(np.std(informednp)))

