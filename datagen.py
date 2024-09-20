import random
import string
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, List, Dict, Union
import numpy as np


def generate_unique_ids(n: int = 10, length: int = 10) -> List[str]:
    """
    Generate a list of unique alphanumeric IDs.

    Parameters:
        n (int): The number of unique IDs to generate.
        length (int): The length of each ID.

    Returns:
        List[str]: A list of unique alphanumeric IDs.
    """
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
    weights_ranges: Optional[List[Dict[str, Union[int, float]]]] = None
) -> List[datetime]:
    """
    Generate a list of random timestamps within a date range, with optional weighted ranges.

    Parameters:
        n (int): Number of timestamps to generate.
        start_date (str): Start date in string format (e.g., 'YYYY-MM-DD').
        end_date (str): End date in string format (e.g., 'YYYY-MM-DD').
        date_format (str): Format of the input dates (default is '%Y-%m-%d').
        weights_ranges (Optional[List[Dict[str, Union[int, float]]]]): Optional list of dictionaries 
            specifying weighted ranges with 'start', 'end', and 'weight' keys.

    Returns:
        List[datetime]: A list of randomly generated timestamps.
    """
    timestamps = []
    start_datetime = datetime.strptime(start_date, date_format)
    end_datetime = datetime.strptime(end_date, date_format)

    if weights_ranges is None:
        # Uniform distribution of timestamps
        total_seconds = int((end_datetime - start_datetime).total_seconds())
        for _ in range(n):
            random_seconds = random.randint(0, total_seconds)
            random_timestamp = start_datetime + timedelta(seconds=random_seconds)
            timestamps.append(random_timestamp)
    else:
        # Weighted distribution of timestamps
        for _ in range(n):
            total_weight = sum(r['weight'] for r in weights_ranges)
            choice = random.choices(weights_ranges, weights=[r['weight'] for r in weights_ranges])[0]

            min_seconds = int(choice['start'] * 365 * 24 * 60 * 60)  # Convert years to seconds
            max_seconds = int(choice['end'] * 365 * 24 * 60 * 60)

            random_seconds = random.randint(min_seconds, max_seconds)
            random_date = start_datetime + timedelta(seconds=random_seconds)

            # Ensure timestamp is within overall date range
            while not (start_datetime <= random_date <= end_datetime):
                random_seconds = random.randint(min_seconds, max_seconds)
                random_date = start_datetime + timedelta(seconds=random_seconds)

            timestamps.append(random_date)

    return timestamps


def generate_random_ints(min_val: int, max_val: int, n: int) -> List[int]:
    """
    Generate a list of random integers within a specified range.

    Parameters:
        min_val (int): The minimum integer value (inclusive).
        max_val (int): The maximum integer value (inclusive).
        n (int): Number of integers to generate.

    Returns:
        List[int]: A list of randomly generated integers.
    """
    return [random.randint(min_val, max_val) for _ in range(n)]


def generate_random_values(
    n: int,
    values: Union[List[str], Dict[str, int]]
) -> List[str]:
    """
    Generate a list of random values from a list or dictionary of weighted values.

    Parameters:
        n (int): Number of random values to generate.
        values (Union[List[str], Dict[str, int]]): List of values for uniform selection or a dictionary
            with values and their corresponding weights.

    Returns:
        List[str]: A list of randomly selected values.
    """
    if isinstance(values, list):
        return [random.choice(values) for _ in range(n)]
    elif isinstance(values, dict):
        value_list = list(values.keys())
        weight_list = list(values.values())
        return random.choices(value_list, weights=weight_list, k=n)


def random_value_in_range(
    lookup_value: str,
    lookup_label: str,
    range_df: pd.DataFrame,
    high_label: str,
    low_label: str
) -> Optional[int]:
    """
    Generate a random integer within a specified range based on a lookup value in a DataFrame.

    Parameters:
        lookup_value (str): The value to search for in the DataFrame.
        lookup_label (str): The column name to use for the lookup.
        range_df (pd.DataFrame): DataFrame containing the ranges.
        high_label (str): Column name for the upper bound of the range.
        low_label (str): Column name for the lower bound of the range.

    Returns:
        Optional[int]: A randomly generated integer within the range, or None if not found.
    """
    row = range_df[range_df[lookup_label] == lookup_value]
    if not row.empty:
        low = row[low_label].values[0]
        high = row[high_label].values[0]
        return np.random.randint(low // 100, high // 100 + 1) * 100
    return None
