import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("..")
import icarus.constants as constants
import icarus.regression as reg

# Load the DataFrame
file = 'Alternative Fuel Vehicles US.csv'
# Load the DataFrame
df = reg.load_dataframe(constants.source_folder + file)

# Print DataFrame info
print(df.info())

DRIVETRAIN = 'Drivetrain'
ALT_FUEL_EFFICIENCY = 'Alternative Fuel Economy Combined'
CONVENTIONAL_FUEL_EFFICIENCY = 'Conventional Fuel Economy Combined'

# Create the averaged fuel efficiency column
df['AVERAGED_FUEL_EFFICIENCY'] = df[[ALT_FUEL_EFFICIENCY, CONVENTIONAL_FUEL_EFFICIENCY]].mean(axis=1)

# Filter for relevant columns
df = df[['Category', 'Model', 'Model Year', 'Manufacturer', 'Fuel', DRIVETRAIN, ALT_FUEL_EFFICIENCY, CONVENTIONAL_FUEL_EFFICIENCY, 'AVERAGED_FUEL_EFFICIENCY']]

# Filter for all-wheel drive SUVs and Sedans
filtered_df = df[(df['Category'].isin(['SUV', 'Sedan/Wagon'])) & (df[DRIVETRAIN] == 'AWD')]

# Define the aspect ratio
aspect_ratio = 12 / 8

# Specify the width and dpi
width = 2000
dpi = 225

# Calculate the height based on the aspect ratio
height = width / aspect_ratio

# Calculate figure size
w,h = reg.calc_fig_size(width, dpi), reg.calc_fig_size(height, dpi)
plt.figure(figsize=(w,h))

sns.violinplot(data=filtered_df, x='Category', y='AVERAGED_FUEL_EFFICIENCY')
plt.title('Fuel Efficiency Comparison: SUVs vs Sedans (All Wheel Drive)')
plt.xlabel('Vehicle Category')
plt.ylabel('Averaged Fuel Efficiency')

plt.savefig(constants.output_folder + 'violinplot.png', dpi=dpi)
