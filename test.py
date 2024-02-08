from Game import Game
import time
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def run():

    informedPlayerScores = []
    randomPlayerScores = []
    rounds = 13
    players = 4
    playerStrengths1 = [2,1,1,1]
    playerStrengths2 = [0,0,0,0]
    verbose = True
    samples = 1
    dynamic_hand = True
    startTime = time.time()
    optimisations =  [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, 13, verbose, optimisations, dynamic_hand=dynamic_hand)
        informedPlayerScores.append(game.getPlayers()[0].getScore())

    sys.stdout = sys.__stdout__
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    informednp = np.array(informedPlayerScores)

    print("informed mean: " + str(np.mean(informednp)))
    print("informed standard deviation: " + str(np.std(informednp)))


if __name__ == "__main__":
    run()