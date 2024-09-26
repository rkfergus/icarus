import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
import icarus.regression as reg
import icarus.constants as constants
import icarus.datagen as dg

from faker import Faker


columns = ['Atendee Name', 'Address', 'RSVP', 'Meal Choice']

rsvp = {'Yes':5, 'No':3, ' ':2}
meal = {'Chicken':5, 'Fish':4, 'Vegetarian':2, 'Vegan':1, 'Gluten Free':1}

n = 100
df = pd.DataFrame(columns=columns)

df['RSVP'] = dg.generate_random_values(n, rsvp)
df['Meal Choice'] = dg.generate_random_values(n, meal)

fake = Faker()
df['Atendee Name'] = [fake.name() for _ in range(n)]
df['Address'] = [fake.address() for _ in range(n)]


df.to_csv(constants.output_folder + 'rsvp_dataset.csv', index=False)


# Count occurrences of each RSVP category
rsvp_counts = df['RSVP'].value_counts()

# Create a pie chart
colors = sns.color_palette('pastel')  # Use Seaborn's color palette
plt.figure(figsize=(6, 6))  # Set the figure size
plt.pie(rsvp_counts, labels=rsvp_counts.index, colors=colors, autopct='%1.1f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')  
plt.savefig(constants.output_folder + 'rsvp_pie_chart.png', dpi=225)
