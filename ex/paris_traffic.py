import sys
sys.path.append("..")
import icarus.regression as reg
import icarus.constants as constants

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the DataFrame
file = 'Paris_-_Paris.csv'
folder = constants.source_folder 
df = reg.load_dataframe(folder + file)


CONGESTION = 'LiveCongestion'
TRAVEL_TIME = 'TravelTimeLive'
JAM_LENGTH = 'JamsLength'
all_cols = [CONGESTION, TRAVEL_TIME, JAM_LENGTH]
df = df[all_cols]
df_pivot = df.pivot_table(JAM_LENGTH, CONGESTION,TRAVEL_TIME)

print(df.describe())

# plt.figure(figsize=(20, 16))
ax = sns.jointplot(y=df[CONGESTION],x=df[TRAVEL_TIME], hue=df[JAM_LENGTH])
plt.tight_layout()
plt.savefig(constants.output_folder + 'heatmap.png')
