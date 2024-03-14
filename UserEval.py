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
plt.plot(easy_scores_np[0], label='Versus Easy Agent')
plt.plot(med_scores_np[0], label='Versus Medium Agent')
plt.plot(hard_scores_np[0], label='Versus Hard Agent')
# Adding labels and title
plt.xlabel('Sample')
plt.ylabel('Player Score')
plt.title(f'Performance Trends of Real Players\' Scores Against Agents in a decreasing hand size card game')
plt.legend()  # Show legend

# Display the plot
plt.show()
avg_easy_score = []
for i in range(0, len(easy_scores_np[1])):
    avg = easy_scores_np[1][i] + easy_scores_np[2][i] + easy_scores_np[3][i]
    avg /= 3
    avg_easy_score.append(avg)
avg_med_score = []
for i in range(0, len(med_scores_np[1])):
    avg = med_scores_np[1][i] + med_scores_np[2][i] + med_scores_np[3][i]
    avg /= 3
    avg_med_score.append(avg)
avg_hard_score = []
for i in range(0, len(hard_scores_np[1])):
    avg = hard_scores_np[1][i] + hard_scores_np[2][i] + hard_scores_np[3][i]
    avg /= 3
    avg_hard_score.append(avg)

plt.plot(avg_easy_score, label='Easy Agent')
plt.plot(avg_med_score, label='Medium Agent')
plt.plot(avg_hard_score, label='Hard Agent')
# Adding labels and title
plt.xlabel('Sample')
plt.ylabel('Player Score')
plt.title(f'Performance Trends of Agents\' Scores Against Real Players and Themselves in a decreasing hand size card game')
plt.legend()  # Show legend

# Display the plot
plt.show()

easy_score_dif = []
for i in range(0, len(easy_scores_np[1])):
    dif = easy_scores_np[0][i] - max(easy_scores_np[1][i], easy_scores_np[2][i], easy_scores_np[3][i])
    easy_score_dif.append(dif)
med_score_dif = []
for i in range(0, len(med_scores_np[1])):
    dif = med_scores_np[0][i] - max(med_scores_np[1][i], med_scores_np[2][i], med_scores_np[3][i])
    med_score_dif.append(dif)
hard_score_dif = []
for i in range(0, len(hard_scores_np[1])):
    dif = hard_scores_np[0][i] - max(hard_scores_np[1][i], hard_scores_np[2][i], hard_scores_np[3][i])
    hard_score_dif.append(dif)

plt.plot(easy_score_dif, label='Easy Agent')
plt.plot(med_score_dif, label='Medium Agent')
plt.plot(hard_score_dif, label='Hard Agent')
plt.axhline(y=0, color='red')
# Adding labels and title
plt.xlabel('Sample')
plt.ylabel('Player Score')
plt.title(f'Differences in Scores Between Real Players and Highest Scoring Agents in a decreasing hand size card game')
plt.legend()  # Show legend

# Display the plot
plt.show()