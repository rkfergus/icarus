import sys
sys.path.append("..")
import icarus.datagen as dg

import pandas as pd 
import numpy as np


def time_str_to_seconds(time_str):
        parts = time_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])  # Convert MM:SS to seconds

def has_concurrent_assignments(df):
    # Helper function to convert MM:SS to seconds
    # Check for concurrent assignments by agent
    for agent_id in df['Agent ID'].unique():
        agent_calls = df[df['Agent ID'] == agent_id].copy()
        # Sort by start time and check for overlaps
        agent_calls = agent_calls.sort_values('start_time')
        # print(agent_calls)
        for i in range(len(agent_calls) - 1):
            if agent_calls.iloc[i]['end_time'] > agent_calls.iloc[i+1]['start_time']:
                print(agent_calls)
                return True
    return False


def data_gen():

    columns = ['Timestamp','Hold Time','Customer ID', 'Complaint Type','Agent ID', 'Call Duration', 'Resolution Status']
    num_rows = 2732 
    num_agents = 237
    df = pd.DataFrame(columns=columns)

    df['Customer ID'] = dg.generate_unique_ids(num_rows,length=15)
    df['Timestamp'] = dg.generate_timestamps(num_rows, '2025-01-01', '2025-03-31')

    complaint_types = {'Billing':27, 'Technical Support':45, 'General Inquiry':12, 'Service Outage':3, 'Account Management':10, 'Feedback':2, 'Cancellation':1}
    df['Complaint Type'] = dg.generate_random_values(num_rows,complaint_types )

    resolution_status = {'Resolved':85, 'Pending':10, 'Escalated':5}
    df['Resolution Status'] = dg.generate_random_values(num_rows, resolution_status)

    # Time constriants in seconds   
    duration_array = np.array([.25,10,1,60]) # duration in mins
    duration_array = np.multiply(duration_array,60).astype(int) # convert to seconds

    df['Hold Time']  = np.array(dg.generate_random_duration(num_rows, min_duration=duration_array[0], max_duration=duration_array[1]))
    df['Call Duration'] = np.array(dg.generate_random_duration(num_rows, min_duration=duration_array[2], max_duration=duration_array[3]))

    df['Hold Time'] = pd.to_timedelta(df['Hold Time'], unit='s')
    df['Call Duration'] = pd.to_timedelta(df['Call Duration'], unit='s')

    df['start_time'] = df['Timestamp'] + df['Hold Time']
    df['end_time'] = df['start_time'] + df['Call Duration']

    # print(df.head(10))

    df['Hold Time'] = df['Hold Time'].apply(lambda x: dg.seconds_to_hms(x,format_str="%M:%S"))
    df['Call Duration'] = df['Call Duration'].apply(lambda x: dg.seconds_to_hms(x,format_str="%M:%S"))


    agent_ids = dg.generate_unique_ids(num_agents,length=10)
    df.sort_values(by='start_time', ascending=True, inplace=True)

    # Track when each agent becomes available
    agent_availability = {agent_id: pd.Timestamp('2025-01-01') for agent_id in agent_ids}
    
    # Assign agents to calls
    for idx, row in df.iterrows():
        # Find agents available before this call starts
        available_agents = [agent_id for agent_id, available_time 
                           in agent_availability.items() 
                           if available_time <= row['start_time']]
        
        if available_agents:
            # Choose a random available agent
            chosen_agent = np.random.choice(available_agents)
        else:
            # If no agents available, choose the one who will be free soonest
            chosen_agent = min(agent_availability, key=agent_availability.get)
        
        # Assign the agent
        df.at[idx, 'Agent ID'] = chosen_agent
        
        # Update when this agent will be available next
        agent_availability[chosen_agent] = row['end_time']
    

    return df

df = data_gen()
max= 10
count = 0

while has_concurrent_assignments(df):
    print("Warning: Found concurrent assignments. Regenerating data...")
    df = data_gen()
    count += 1
    if count > max:
        print("Error: Too many attempts to generate unique assignments.")
        break


output_file = f'andromeda/service_calls.csv'
print(f"Output file: {output_file}")
df.to_csv(output_file, index=False)


