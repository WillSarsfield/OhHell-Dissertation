from Game import Game
import time
import sys, os
import numpy as np
import matplotlib as plt

informedPlayerScores = []
randomPlayerScores = []
rounds = 26
players = 4
playerStrengths1 = [1,0,0,0]
playerStrengths2 = [0,0,0,0]
verbose = False
samples = 100
startTime = time.time()
for i in range(0, samples):
    game = Game(rounds, players, playerStrengths1, verbose)
    informedPlayerScores.append(game.getPlayers()[0].getScore())
for i in range(0, samples):
    game = Game(rounds, players, playerStrengths2, verbose)
    randomPlayerScores.append(game.getPlayers()[0].getScore())
sys.stdout = sys.__stdout__
print("---%s seconds---" % (time.time() - startTime))
print("Rounds played: " + str(rounds))
informednp = np.array(informedPlayerScores)
randomnp = np.array(randomPlayerScores)
print("informed mean: " + str(np.mean(informednp)))
print("informed standard deviation: " + str(np.std(informednp)))
print("random mean: " + str(np.mean(randomnp)))
print("random standard deviation: " + str(np.std(randomnp)))
