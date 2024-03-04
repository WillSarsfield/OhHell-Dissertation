import csv
import matplotlib.pyplot as plt
import numpy as np

with open("scores.csv", "r") as file:
    csv_reader = csv.reader(file, delimiter='\t')
    easy_scores = [[],[],[],[]]
    med_scores = [[],[],[],[]]
    hard_scores = [[],[],[],[]]
    for row in csv_reader:
        row = [int(value) for value in row]
        if row[3] == 0:
            for i in range(4,8):
                easy_scores[i-4].append(row[i])
        elif row[3] == 1:
            for i in range(4,8):
                med_scores[i-4].append(row[i])
        elif row[3] == 2:
            for i in range(4,8):
                hard_scores[i-4].append(row[i])
easy_scores_np = []
med_scores_np = []
hard_scores_np = []
for i in range(0,4):
    easy_scores_np.append(np.array(easy_scores[i]))
    med_scores_np.append(np.array(med_scores[i]))
    hard_scores_np.append(np.array(hard_scores[i]))

print(f"player average against easy: {np.mean(easy_scores_np[0])} / std: {np.std(easy_scores_np[0])}")
print(f"easy bot average against player and themselves: {np.mean(np.ravel(easy_scores_np[1:4]))} / std: {np.std(np.ravel(easy_scores_np[1:4]))}")
print(f"player average against medium: {np.mean(med_scores_np[0])} / std: {np.std(med_scores_np[0])}")
print(f"medium bot average against player and themselves: {np.mean(np.ravel(med_scores_np[1:4]))} / std: {np.std(np.ravel(med_scores_np[1:4]))}")
print(f"player average against hard: {np.mean(hard_scores_np[0])} / std: {np.std(hard_scores_np[0])}")
print(f"hard bot average against player and themselves: {np.mean(np.ravel(hard_scores_np[1:4]))} / std: {np.std(np.ravel(hard_scores_np[1:4]))}")
