from Game import Game
import time
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def run():

    bestPlayerScores = []
    informedPlayer1Scores = []
    informedPlayer2Scores = []
    informedPlayer3Scores = []
    randomPlayerScores = []
    rounds = 6
    players = 4
    playerStrengths1 = [2,1,1,1]
    playerStrengths2 = [0,0,0,0]
    verbose = False
    samples = 10
    startTime = time.time()
    optimisations =  [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, 4, verbose, optimisations)
        bestPlayerScores.append(game.getPlayers()[0].getScore())
        informedPlayer1Scores.append(game.getPlayers()[1].getScore())
        informedPlayer2Scores.append(game.getPlayers()[2].getScore())
        informedPlayer3Scores.append(game.getPlayers()[3].getScore())
        sys.stdout = sys.__stdout__
        print(f"samples complete: {i+1}/{samples}")
        print(print("---%s seconds---" % (time.time() - startTime)))
    print("Best vs informed finished")
    print("---%s seconds---" % (time.time() - startTime))
    print(f"Rounds played: {rounds}, Samples: {samples}")
    startTime = time.time()
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths2, 4, verbose, optimisations)
        randomPlayerScores.append(game.getPlayers()[0].getScore())
    sys.stdout = sys.__stdout__
    print("random vs random finished")
    print("---%s seconds---" % (time.time() - startTime))
    print(f"Rounds played: {rounds}, Samples: {samples}")
    bestnp = np.array(bestPlayerScores)
    informed1np = np.array(informedPlayer1Scores)
    informed2np = np.array(informedPlayer2Scores)
    informed3np = np.array(informedPlayer3Scores)
    randomnp = np.array(randomPlayerScores)
    print("best agent mean: " + str(np.mean(bestnp)))
    print("best standard deviation: " + str(np.std(bestnp)))
    print("informed player 1 mean: " + str(np.mean(informed1np)))
    print("informed player 1 standard deviation: " + str(np.std(informed1np)))
    print("informed player 2 mean: " + str(np.mean(informed2np)))
    print("informed player 2 standard deviation: " + str(np.std(informed2np)))
    print("informed player 3 mean: " + str(np.mean(informed3np)))
    print("informed player 3 standard deviation: " + str(np.std(informed3np)))
    print("random player mean: " + str(np.mean(randomnp)))
    print("random player deviation: " + str(np.std(randomnp)))
    plt.plot(bestPlayerScores, label='Best Agent')
    plt.plot(informedPlayer1Scores, label='Informed Player 1')
    plt.plot(informedPlayer2Scores, label='Informed Player 2')
    plt.plot(informedPlayer3Scores, label='Informed Player 3')
    plt.plot(randomPlayerScores, label='Random Player')
    # Adding labels and title
    plt.xlabel('Sample')
    plt.ylabel('Player Score')
    plt.title('Performance Trends of Best Agent and Informed Players in a 4 card game')
    plt.legend()  # Show legend

    # Display the plot
    plt.show()


if __name__ == "__main__":
    run()