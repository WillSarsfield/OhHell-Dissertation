import optuna
import time
from Game import Game
import sys
import numpy as np

def normalise(weights):
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
    return weights


def objective(trial):
    weights = []
    best_weights = [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
    if trial.number == 0:
        weights = [0.285903516922823, 0.1343298885883228, 0.2513171910666505, 0.2654805206104466, 0.06296888281175703, 0.19781578320406684, 0.40322548219933846, 0.1057952046865951, 0.29316352990999955, 0.24951563665051385, 0.25987660163497556, 0.23694603672039563, 0.25366172499411493]
        for i, weight in enumerate(weights):
            trial.suggest_categorical(f'weight_{i}', [weight])
    else:
        for i in range(13):
            weights.append(trial.suggest_float(f'weight{i}', 0, 1))
        weights = normalise(weights)

    score = run_game(weights, best_weights)

    return score

def run_game(weights, best_weights):
    informedPlayerScores = []
    rounds = 26
    players = 4
    playerStrengths1 = [1,1,1,1]
    verbose = False
    samples = 200
    startTime = time.time()
    optimisations = weights
    for i in range(0, samples):
        game = Game(rounds, players, playerStrengths1, verbose, optimisations, best_weights)
        informedPlayerScores.append(game.getPlayers()[0].getScore())
    sys.stdout = sys.__stdout__
    print("---%s seconds---" % (time.time() - startTime))
    print("Rounds played: " + str(rounds))
    informednp = np.array(informedPlayerScores)
    print(f"informed mean: {np.mean(informednp)}")
    return np.mean(informednp)

if __name__ == "__main__":
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=200)

    print("Best trial:")
    trial = study.best_trial
    print("  Value: ", trial.value)
    print("  Params: ")
    weights = []
    for key, value in trial.params.items():
        weights.append(value)
    weights = normalise(weights)
    print(weights)
