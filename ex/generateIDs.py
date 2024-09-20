import sys
sys.path.append("..")
import icarus.datagen as dg

import pandas as pd 



columns = ['Timestamp','Device ID','Device Cost', 'Device Name','Cost Center','Employee ID', 'Action']
num_rows = 100 

df = pd.DataFrame(columns=columns)

df['Device ID'] = dg.generate_unique_ids(num_rows,length=10)
df['Employee ID'] = dg.generate_unique_ids(num_rows,length=15)
df['Timestamp'] = dg.generate_timestamps(num_rows, '2023-01-01', '2024-06-30')


device_details = pd.read_csv('ex/src/device_details.csv')

cost_centers = ['Finance', 'HR', 'IT', 'Marketing', 'Sales', 'Operations', 'R&D', 'Customer Service', 'Legal', 'Product Development']
actions = ['New', 'Renew', 'Return']
df['Cost Center'] = dg.generate_random_values(num_rows, cost_centers)
df['Action'] = dg.generate_random_values(num_rows, actions)


# Assuming 'device_details.csv' includes a column 'ID Start' which is the first character of 'Device ID'
device_details = pd.read_csv('ex/src/device_details.csv')

# Extract the first character from 'Device ID' in df
df['ID Start'] = df['Device ID'].str[0]

# Merge df and device_details on 'ID Start'
merged_df = pd.merge(df, device_details, on='ID Start', how='left')

# Fill in 'Device Name' and 'Device Cost' in df from merged_df
df['Device Name'] = merged_df['Manufacturer'] + " - " + merged_df['Model']
df['Device Cost'] = merged_df['Cost']

# Drop 'ID Start' if not needed
df.drop(columns=['ID Start'], inplace=True)

df.to_csv(f'ex/out/output_{dg.generate_unique_ids(1,3)[0]}.csv')