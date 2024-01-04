from Game import Game
import time
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def run():

    informedPlayerScores = []
    randomPlayerScores = []
    rounds = 26
    players = 4
    playerStrengths1 = [1,1,1,1]
    playerStrengths2 = [0,0,0,0]
    verbose = False
    samples = 200
    startTime = time.time()
    optimisations =  [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, verbose, optimisations, optimisations)
        informedPlayerScores.append(game.getPlayers()[0].getScore())
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths2, verbose)
        randomPlayerScores.append(game.getPlayers()[0].getScore())
    sys.stdout = sys.__stdout__
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    informednp = np.array(informedPlayerScores)
    randomnp = np.array(randomPlayerScores)
    plt.plot(informedPlayerScores, label='Informed Player mk 2')
    plt.plot(randomPlayerScores, label='Random Player')

    # Adding labels and title
    plt.xlabel('Sample')
    plt.ylabel('Player Score')
    plt.title('Performance Trends of Informed and Random Players')
    plt.legend()  # Show legend

    # Display the plot
    plt.show()
    print("informed mean: " + str(np.mean(informednp)))
    print("informed standard deviation: " + str(np.std(informednp)))
    print("random mean: " + str(np.mean(randomnp)))
    print("random standard deviation: " + str(np.std(randomnp)))


if __name__ == "__main__":
    run()