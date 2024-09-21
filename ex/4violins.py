import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys

# Local imports
sys.path.append("..")
import icarus.regression as reg
import icarus.constants as constants

# Constants
FILE_NAME = 'Alternative Fuel Vehicles US.csv'
OUTPUT_FILE = 'violinplot_fuel_comparison.png'
DRIVETRAIN = 'Drivetrain'
ALT_FUEL_EFFICIENCY = 'Alternative Fuel Economy Combined'
CONVENTIONAL_FUEL_EFFICIENCY = 'Conventional Fuel Economy Combined'
COLUMNS_TO_KEEP = [
    'Category', 'Model', 'Model Year', 'Manufacturer', 'Fuel', 
    DRIVETRAIN, ALT_FUEL_EFFICIENCY, CONVENTIONAL_FUEL_EFFICIENCY, 
    'AVERAGED_FUEL_EFFICIENCY'
]

# Load the DataFrame
df = reg.load_dataframe(constants.source_folder + FILE_NAME)

# Print DataFrame info
print(df.info())

# Create the averaged fuel efficiency column
df['AVERAGED_FUEL_EFFICIENCY'] = df[[ALT_FUEL_EFFICIENCY, CONVENTIONAL_FUEL_EFFICIENCY]].mean(axis=1)

# Filter for relevant columns
df = df[COLUMNS_TO_KEEP]

# Filter for all-wheel drive SUVs and Sedans
filtered_df = df[(df['Category'].isin(['SUV', 'Sedan/Wagon'])) & (df[DRIVETRAIN] == 'AWD')]

# Create a melted DataFrame for plotting
melted_df = filtered_df.melt(
    id_vars=['Category'], 
    value_vars=[ALT_FUEL_EFFICIENCY, CONVENTIONAL_FUEL_EFFICIENCY], 
    var_name='Fuel_Type', 
    value_name='Fuel_Efficiency'
)
# Define the aspect ratio
aspect_ratio = 12 / 8

# Specify the width and dpi
width = 2000
dpi = 225

# Calculate the height based on the aspect ratio
height = width / aspect_ratio

# Calculate figure size
fig_size = reg.calc_fig_size(width, dpi)

# Plot the data
plt.figure(figsize=(fig_size, height / dpi))
violin_plot = sns.violinplot(data=melted_df, x='Category', y='Fuel_Efficiency', hue='Fuel_Type', split=True)




# Move the legend outside the plot
plt.legend(
    title='Fuel Type',
    loc='upper right',
    fontsize='small',
    title_fontsize='medium',
    frameon=True,
    fancybox=True
)
# Set custom labels for the legend
new_labels = ['Alternative Fuel', 'Conventional Fuel']
for t, l in zip(violin_plot.legend_.texts, new_labels):
    t.set_text(l)

plt.title('Fuel Efficiency Comparison: SUVs vs Sedans (All Wheel Drive)')
plt.xlabel('Vehicle Category')
plt.ylabel('Fuel Efficiency')


# Save the plot
plt.savefig(constants.output_folder + OUTPUT_FILE, dpi=dpi)
print(f"Plot saved to {constants.output_folder + OUTPUT_FILE}")