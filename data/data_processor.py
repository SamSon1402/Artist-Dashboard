"""Utilities for processing and transforming data."""
import pandas as pd
from datetime import datetime, timedelta

def convert_to_weekly(data, date_column, value_column):
    """Convert daily data to weekly aggregated data."""
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_dtype(data[date_column]):
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Add week number
    data['week'] = data[date_column].dt.isocalendar().week
    data['year'] = data[date_column].dt.isocalendar().year
    
    # Group by week and year
    weekly_data = data.groupby(['year', 'week']).agg({
        value_column: 'sum',
        date_column: 'first'  # Take the first day of each week for the x-axis
    }).reset_index()
    
    return weekly_data

def convert_to_monthly(data, date_column, value_column):
    """Convert daily data to monthly aggregated data."""
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_dtype(data[date_column]):
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Add month and year
    data['month'] = data[date_column].dt.month
    data['year'] = data[date_column].dt.year
    
    # Group by month and year
    monthly_data = data.groupby(['year', 'month']).agg({
        value_column: 'sum',
        date_column: 'first'  # Take the first day of each month for the x-axis
    }).reset_index()
    
    return monthly_data

def calculate_growth_rate(data, value_column):
    """Calculate period-over-period growth rates."""
    data = data.copy()
    data['previous_value'] = data[value_column].shift(1)
    data['growth_rate'] = (data[value_column] - data['previous_value']) / data['previous_value']
    return data

def calculate_moving_average(data, value_column, window=7):
    """Calculate moving average for the specified column."""
    data = data.copy()
    data[f'{value_column}_ma{window}'] = data[value_column].rolling(window=window).mean()
    return data

def filter_by_date_range(data, date_column, start_date, end_date):
    """Filter data by date range."""
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_dtype(data[date_column]):
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Convert start_date and end_date to datetime if they are strings
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    # Filter data
    filtered_data = data[(data[date_column] >= start_date) & (data[date_column] <= end_date)]
    
    return filtered_data

def pivot_data(data, index, columns, values, aggfunc='sum'):
    """Create a pivot table from the data."""
    return pd.pivot_table(data, index=index, columns=columns, values=values, aggfunc=aggfunc)

def calculate_percentages(data, value_column, total=None):
    """Calculate percentages for the specified column."""
    data = data.copy()
    if total is None:
        total = data[value_column].sum()
    
    data[f'{value_column}_pct'] = data[value_column] / total * 100
    return data