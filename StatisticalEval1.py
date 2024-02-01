from Game import Game
import time
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def run():

    bestPlayerScores = []
    informedPlayerScores = []
    rounds = 6
    players = 4
    playerStrengths1 = [2,1,1,1]
    playerStrengths2 = [1,1,1,1]
    verbose = True
    samples = 10
    startTime = time.time()
    optimisations =  [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, 4, verbose, optimisations)
        bestPlayerScores.append(game.getPlayers()[0].getScore())
        print(f"samples complete: {i+1}/{samples}")
        print(print("---%s seconds---" % (time.time() - startTime)))
    print("Best vs informed finished")
    print("---%s seconds---" % (time.time() - startTime))
    print(f"Rounds played: {rounds}, Samples: {samples}")
    verbose = False
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths2, verbose)
        informedPlayerScores.append(game.getPlayers()[0].getScore())
    sys.stdout = sys.__stdout__
    print("informed vs informed finished")
    print("---%s seconds---" % (time.time() - startTime))
    print(f"Rounds played: {rounds}, Samples: {samples}")
    bestnp = np.array(bestPlayerScores)
    informednp = np.array(informedPlayerScores)
    print("informed mean: " + str(np.mean(informednp)))
    print("informed standard deviation: " + str(np.std(informednp)))
    print("random mean: " + str(np.mean(informednp)))
    print("random standard deviation: " + str(np.std(informednp)))
    plt.plot(bestPlayerScores, label='Best Agent vs Informed players')
    plt.plot(informedPlayerScores, label='Informed Player vs Informed Players')

    # Adding labels and title
    plt.xlabel('Sample')
    plt.ylabel('Player Score')
    plt.title('Performance Trends of Best Agent and Informed Players in a 4 card game')
    plt.legend()  # Show legend

    # Display the plot
    plt.show()


if __name__ == "__main__":
    run()