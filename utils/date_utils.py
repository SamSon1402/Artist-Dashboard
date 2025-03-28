"""Utilities for date manipulation and formatting."""
import pandas as pd
from datetime import datetime, timedelta

def get_date_range(start_date, end_date=None):
    """Get a list of dates between start_date and end_date."""
    if end_date is None:
        end_date = datetime.now()
    
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    days = (end_date - start_date).days + 1
    date_list = [start_date + timedelta(days=i) for i in range(days)]
    
    return date_list

def get_days_from_period(time_period):
    """Convert a time period string to number of days."""
    if time_period == "Last 7 Days":
        return 7
    elif time_period == "Last 30 Days":
        return 30
    elif time_period == "Last 90 Days":
        return 90
    elif time_period == "Last 6 Months":
        return 180
    elif time_period == "Last Year":
        return 365
    else:
        return 30  # Default to 30 days

def get_date_range_for_period(time_period):
    """Get start and end dates for a given time period."""
    days = get_days_from_period(time_period)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    
    return start_date, end_date

def format_date(date, format_str="%Y-%m-%d"):
    """Format a date object as a string."""
    if isinstance(date, str):
        date = pd.to_datetime(date)
    
    return date.strftime(format_str)

def get_month_name(month_num):
    """Get the name of a month from its number."""
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return month_names[month_num - 1]

def get_short_month_name(month_num):
    """Get the short name of a month from its number."""
    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    return month_names[month_num - 1]

def get_weekday_name(weekday_num):
    """Get the name of a weekday from its number."""
    weekday_names = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    return weekday_names[weekday_num]

def add_date_parts(df, date_column):
    """Add year, month, day, and day of week columns to a dataframe."""
    df = df.copy()
    
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Add date parts
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    df['weekday'] = df[date_column].dt.weekday
    df['weekday_name'] = df['weekday'].apply(get_weekday_name)
    df['month_name'] = df['month'].apply(get_short_month_name)
    
    return df