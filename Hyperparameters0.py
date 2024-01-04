import optuna
import time
from Game import Game
import sys
import numpy as np

def objective(trial):
    weights = []
    if trial.number == 0:
        weights = [0.1,0.45,0.15,0.15,0.15,0.2,0.4,0.2,0.2,0.2,0.4,0.25,0.15]
    else:
        for i in range(13):
            weights.append(trial.suggest_float(f'weight{i}', 0, 1))
        total = 0
        for i in range(0,5):
            total += weights[i]
        for i in range(0,5):
            weights[i] = weights[i]/total
        total = 0
        for i in range(5,9):
            total += weights[i]
        for i in range(5,9):
            weights[i] = weights[i]/total
        total = 0
        for i in range(9,13):
            total += weights[i]
        for i in range(9,13):
            weights[i] = weights[i]/total
    
    score = run_game(weights)


    return score

def run_game(weights):
    informedPlayerScores = []
    rounds = 26
    players = 4
    playerStrengths1 = [1,0,0,0]
    verbose = False
    samples = 100
    startTime = time.time()
    optimisations = [weights]
    weights.append(optimisations)
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, verbose, optimisations)
        informedPlayerScores.append(game.getPlayers()[0].getScore())
    sys.stdout = sys.__stdout__
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    informednp = np.array(informedPlayerScores)
    print(f"informed mean: {np.mean(informednp)}")
    return np.mean(informednp)

if __name__ == "__main__":
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=1000)

    print("Best trial:")
    trial = study.best_trial
    print("  Value: ", trial.value)
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
