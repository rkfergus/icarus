import random
import string
from datetime import datetime, timedelta
import pandas as pd 
from typing import Optional, List, Dict, Union
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np


def generate_unique_ids(n=10, length=10):
    ids = set()
    while len(ids) < n:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        ids.add(new_id)
    return list(ids)

def generate_timestamps(
    n: int,
    start_date: str,
    end_date: str,
    date_format: str = '%Y-%m-%d',
    weights_ranges: Optional[List[Dict[str, any]]] = None
) -> List[datetime]:
    """
    Generate a list of random timestamps within a range of dates with optional varying frequencies.

    Parameters:
        n (int): Number of timestamps to generate
        start_date (str): The start date in string format.
        end_date (str): The end date in string format.
        date_format (str): The format of the input dates (default is '%Y-%m-%d').
        weights_ranges (Optional[List[Dict[str, any]]]): Optional parameter with weights and ranges. 
            Each dictionary should have 'start', 'end', and 'weight' keys.

    Returns:
        list: A list of randomly generated timestamps within the specified range.
    """
    timestamps = []
    start_datetime = datetime.strptime(start_date, date_format)
    end_datetime = datetime.strptime(end_date, date_format)

    if weights_ranges is None:
        # Uniformly distribute timestamps if no weights_ranges are provided
        total_seconds = int((end_datetime - start_datetime).total_seconds())
        for _ in range(n):
            random_seconds = random.randint(0, total_seconds)
            random_timestamp = start_datetime + timedelta(seconds=random_seconds)
            timestamps.append(random_timestamp)
    else:
        # Generate weighted timestamps
        for _ in range(n):
            # Choose a range based on the weights
            total_weight = sum(r['weight'] for r in weights_ranges)
            choice = random.choices(weights_ranges, weights=[r['weight'] for r in weights_ranges])[0]
            
            # Calculate the range in seconds
            min_seconds = choice['start'] * 365 * 24 * 60 * 60  # Convert years to seconds
            max_seconds = choice['end'] * 365 * 24 * 60 * 60  # Convert years to seconds
            
            # Generate a random number of seconds within the chosen range
            random_seconds = random.randint(min_seconds, max_seconds)
            random_date = start_datetime + timedelta(seconds=random_seconds)
            
            # Ensure the generated date is within the overall range
            if start_datetime <= random_date <= end_datetime:
                timestamps.append(random_date)
            else:
                # If the date is outside the range, retry
                while not (start_datetime <= random_date <= end_datetime):
                    random_seconds = random.randint(min_seconds, max_seconds)
                    random_date = start_datetime + timedelta(seconds=random_seconds)
    
    return timestamps

def random_ints(a, b, n):
    out = list()
    while len(out) < n:
        out.append( random.randint(a,b))
    
    return out

def generate_random_values(
    n: int,
    values: Union[List[str], Dict[str, int]]
) -> List[str]:
    """
    Generate a list of random values based on provided values or weighted values.

    Parameters:
        n (int): Number of random values to generate
        values (Union[List[str], Dict[str, int]]): Either a list of values or a dictionary
            with values as keys and weights as values.

    Returns:
        list: A list of randomly generated values.
    """
    if isinstance(values, list):
        # Uniformly random selection if values is a list
        return [random.choice(values) for _ in range(n)]
    elif isinstance(values, dict):
        # Weighted random selection if values is a dict
        value_list = list(values.keys())
        weight_list = list(values.values())
        return random.choices(value_list, weights=weight_list, k=n)


def random_in_range(lookup_value, lookup_label, range_df, high_label, low_label):
    # Find the row matching the title
    row = range_df[range_df[lookup_label] == lookup_value]
    if not row.empty:
        low = row[high_label].values[0]
        high = row[low_label].values[0]
        result = np.random.randint(low // 100, high // 100 + 1) * 100
        return result




