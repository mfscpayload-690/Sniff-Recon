"""
csv_parser.py

Parser for .csv files using Pandas.
Converts rows to JSON.
"""

import pandas as pd

def parse_csv(file_path):
    """
    Parse a CSV file and convert rows to JSON.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries representing CSV rows.
    """
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')
