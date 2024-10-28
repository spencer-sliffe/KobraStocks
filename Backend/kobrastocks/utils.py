# Backend/kobrastocks/utils.py

from datetime import datetime
import numpy as np
import pandas as pd


def format_date(date_str):
    """
    Converts a date string into a more readable format.
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return date_str


def parse_stock_data(raw_data):
    """
    Parse raw stock data from an external API into a clean format.
    """
    return {
        'ticker': raw_data.get('ticker'),
        'open': raw_data.get('open_price'),
        'close': raw_data.get('close_price'),
        'high': raw_data.get('high_price'),
        'low': raw_data.get('low_price'),
        'volume': raw_data.get('volume'),
    }


def calculate_percentage_change(old_value, new_value):
    """
    Utility function to calculate the percentage change between two values.
    """
    if old_value == 0:
        return None
    try:
        return ((new_value - old_value) / old_value) * 100
    except TypeError:
        return None


def convert_to_builtin_types(obj):
    if isinstance(obj, dict):
        return {k: convert_to_builtin_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_builtin_types(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Timedelta):
        return obj.total_seconds()
    else:
        return obj

