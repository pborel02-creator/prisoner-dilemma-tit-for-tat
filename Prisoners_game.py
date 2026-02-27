import numpy as np
import matplotlib.pyplot as plt

# Score matrix
CC = 3  # Both cooperate
CD = 0  # A cooperates, B defects
DD = 1  # Both defect
DC = 5  # A defects, B cooperates

games = 10000
rounds = 50

# Initialize B's moves: Randomly choose between 'C' (Cooperate) and 'D' (Defect)
# B plays a random strategy
B_moves = np.random.choice(["C","D"], size=(games, rounds))
B_moves[:,0] = 'C' # Both start by cooperating

# Initialize A's moves: Tit-for-Tat strategy
# A starts with 'C', then copies B's previous move
A_moves = np.empty_like(B_moves, dtype=str)
A_moves[:,0] = 'C'
A_moves[:,1:] = B_moves[:,:-1]

# Initialize points arrays
points_A = np.zeros_like(B_moves, dtype=int)
points_B = np.zeros_like(B_moves, dtype=int)

# Scoring logic using masks
# Both cooperate
mask = (A_moves == 'C') & (B_moves == 'C')
points_A[mask] = CC
points_B[mask] = CC

# Both defect
mask = (A_moves == 'D') & (B_moves == 'D')
points_A[mask] = DD
points_B[mask] = DD

# A cooperates, B defects
mask = (A_moves == 'C') & (B_moves == 'D')
points_A[mask] = CD
points_B[mask] = DC

# B cooperates, A defects
mask = (A_moves == 'D') & (B_moves == 'C')
points_A[mask] = DC
points_B[mask] = CD

# Calculate total score per game
total_score_A = np.sum(points_A, axis=1)
total_score_B = np.sum(points_B, axis=1)

csi_A = total_score_A
csi_B = total_score_B
ii = np.arange(1, games + 1)
samp_av_A = np.cumsum(csi_A)/ii
print(f'Final average result A: {samp_av_A[-1]:.3f}')
samp_av_B = np.cumsum(csi_B)/ii
print(f'Final average result B: {samp_av_B[-1]:.3f}')
samp_av2_A = np.cumsum(csi_A**2) / ii
vari_A = (samp_av2_A - samp_av_A**2) * ii/(ii-1)
vari_A[0] = 0
rsd_A = np.sqrt(vari_A/ii)/abs(samp_av_A)
PRSD_A = rsd_A*100
print(f"Final PRSD A: {PRSD_A[-1]:.3f} %")
samp_av2_B = np.cumsum(csi_B**2) / ii
vari_B = (samp_av2_B - samp_av_B**2) * ii/(ii-1)
vari_B[0] = 0
rsd_B = np.sqrt(vari_B/ii)/abs(samp_av_B)
PRSD_B = rsd_B*100
print(f"Final PRSD B: {PRSD_B[-1]:.3f} %")

plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(samp_av_A, label = 'Strategy A (Tit-for-Tat)')
plt.plot(samp_av_B, label = 'Strategy B (Random)')
plt.ylabel('Running Average Score')
plt.xlabel('Number of Experiments (Games)')
plt.title('Convergence of Mean Scores')
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(PRSD_A, label='Strategy A (Tit-for-Tat)')
plt.plot(PRSD_B, label='Strategy B (Random)')
plt.axhline(y=1.0, color='r', linestyle='--', label='1% Threshold')
plt.ylabel('PRSD %')
plt.xlabel('Number of Experiments (Games)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Win/Loss/Draw calculation
wins_A = total_score_A > total_score_B
wins_B = total_score_B > total_score_A
draws = total_score_A == total_score_B

total_wins_A = np.sum(wins_A)
total_wins_B = np.sum(wins_B)
total_draws = np.sum(draws)

perc_wins_A = 100*total_wins_A/games
perc_wins_B = 100*total_wins_B/games
perc_draws = 100*total_draws/games

print("-" * 30)
print(f"Win Percentage A: {perc_wins_A:.2f} %")
print(f"Win Percentage B: {perc_wins_B:.2f} %")
print(f"Draw Percentage: {perc_draws:.2f} %")