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

print('Generating Plot...')
output_file = constants.output_folder + 'heatmap.png'


# Create the jointplot & calculate size
dpi = 225
fig_size = reg.calc_fig_size(1250,dpi)
g = sns.jointplot(y=df[CONGESTION], x=df[TRAVEL_TIME], hue=df[JAM_LENGTH], height=fig_size)

plt.savefig(output_file, dpi=dpi)


print(f"Figure saved to {output_file}")
plt.close()