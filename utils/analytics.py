"""Utilities for performing analytics calculations."""
import numpy as np
import pandas as pd

def calculate_growth(current, previous):
    """Calculate percentage growth between two values."""
    if previous == 0:
        return float('inf')  # Avoid division by zero
    
    return (current - previous) / previous

def calculate_growth_pct(current, previous):
    """Calculate percentage growth between two values as a percentage string."""
    growth = calculate_growth(current, previous)
    
    if growth == float('inf'):
        return "+∞%"
    
    sign = "+" if growth >= 0 else ""
    return f"{sign}{growth:.1%}"

def calculate_running_average(data, column, window=7):
    """Calculate running average of a column."""
    return data[column].rolling(window=window).mean()

def calculate_cumulative_sum(data, column):
    """Calculate cumulative sum of a column."""
    return data[column].cumsum()

def calculate_conversion_rate(numerator, denominator):
    """Calculate conversion rate between two metrics."""
    if denominator == 0:
        return 0
    
    return numerator / denominator

def calculate_retention(initial_value, current_value):
    """Calculate retention rate."""
    if initial_value == 0:
        return 0
    
    return current_value / initial_value

def calculate_churn(initial_value, current_value):
    """Calculate churn rate."""
    if initial_value == 0:
        return 0
    
    return 1 - (current_value / initial_value)

def calculate_engagement_score(streams, saves, shares, completion_rate):
    """Calculate an overall engagement score based on multiple metrics."""
    # Normalize values to a 0-1 scale
    normalized_streams = min(streams / 10000, 1)  # Assuming 10K streams is high engagement
    normalized_saves = min(saves / (streams * 0.3), 1)  # Assuming 30% save rate is high
    normalized_shares = min(shares / (streams * 0.05), 1)  # Assuming 5% share rate is high
    
    # Weight metrics and calculate score
    weights = [0.4, 0.2, 0.2, 0.2]  # Weights for streams, saves, shares, completion_rate
    score = (
        normalized_streams * weights[0] +
        normalized_saves * weights[1] +
        normalized_shares * weights[2] +
        completion_rate * weights[3]
    )
    
    # Return a 0-100 score
    return score * 100

def calculate_percentile(data, value, column=None):
    """Calculate the percentile rank of a value in a dataset."""
    if column is not None:
        data = data[column]
    
    return sum(data <= value) / len(data) * 100

def predict_future_value(data, column, periods=1, method='linear'):
    """Predict future values based on historical data."""
    if method == 'linear':
        # Simple linear regression
        x = np.arange(len(data))
        y = data[column].values
        
        # Calculate slope and intercept
        slope, intercept = np.polyfit(x, y, 1)
        
        # Predict future values
        future_x = np.arange(len(data), len(data) + periods)
        future_y = slope * future_x + intercept
        
        return future_y
    
    elif method == 'moving_average':
        # Moving average prediction
        window = min(7, len(data))  # Default to 7 days or less if not enough data
        ma = data[column].rolling(window=window).mean().iloc[-1]
        
        return [ma] * periods
    
    else:
        raise ValueError(f"Prediction method '{method}' not supported")