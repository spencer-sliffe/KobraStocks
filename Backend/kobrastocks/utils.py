from datetime import datetime

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
