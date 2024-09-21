import sys
sys.path.append("..")
import icarus.constants as constants
import icarus.regression as reg

# Compare phone purchasing behaviors across different age brackets. Identify patterns in storage increase preference, functional status of previous phones, price sensitivity and camera quality consideration. How do these behaviors vary among the age groups?

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

source_folder = constants.source_folder
df = pd.read_csv(source_folder+'phone_buying_preference1.csv')
print(df.info())





def getPlot(df):
    width = 3500
    dpi = 225
    aspect_ratio = 15 / 10

    # Calculate the height based on the aspect ratio
    height = width / aspect_ratio

    # Calculate figure size
    w,h = reg.calc_fig_size(width, dpi), reg.calc_fig_size(height, dpi)


    categories = ['Storage Direction', 'Functionality', 'Price Direction', 'Camera Importance']
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(w,h))
    axes = axes.flatten()

    for i, category in enumerate(categories):
        grouped = df.groupby('Age Group')[category].value_counts().reset_index(name='count')
        # pivot_df = df.pivot_table(index='Age Group', columns=category, aggfunc='size', fill_value=0)
        
        ax = sns.barplot(x='Age Group', y='count', hue=category, data=grouped, palette='muted', ax=axes[i], orient='v')
        ax.set_title(category)
        ax.set_ylabel('Count')
        ax.set_xlabel('Age Group')

    # Adjust layout
    plt.tight_layout()

    # Save the figure
    output_file = constants.output_folder + 'barplots.png'
    plt.savefig(output_file, dpi=dpi)


getPlot(df)