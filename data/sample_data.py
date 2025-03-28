import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_date_range(days, end_date=None):
    """Generate a date range for the specified number of days."""
    if end_date is None:
        end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    return [start_date + timedelta(days=i) for i in range(days)]

def generate_streaming_data(days=30, end_date=None):
    """Generate sample streaming data for the specified time period."""
    dates = get_date_range(days, end_date)
    
    # Generate streaming data with a slight upward trend and weekend boost
    streams = []
    followers = []
    base_streams = 1000
    base_followers = 5000
    
    for i, date in enumerate(dates):
        # Weekend boost (Saturday and Sunday)
        weekend_boost = 1.3 if date.weekday() >= 5 else 1.0
        
        # Random fluctuation
        fluctuation = random.uniform(0.85, 1.15)
        
        # General upward trend
        trend = 1 + (i * 0.01)
        
        # Calculate daily streams
        daily_streams = int(base_streams * weekend_boost * fluctuation * trend)
        streams.append(daily_streams)
        
        # Calculate cumulative followers with some randomness
        daily_new_followers = int(daily_streams * 0.02 * random.uniform(0.8, 1.2))
        base_followers += daily_new_followers
        followers.append(base_followers)
    
    # Create DataFrame
    df_streams = pd.DataFrame({
        'date': dates,
        'streams': streams,
        'followers': followers
    })
    
    return df_streams

def generate_platform_data(total_streams):
    """Generate platform distribution data."""
    platforms = ['Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 'Other']
    platform_pct = [0.45, 0.25, 0.15, 0.10, 0.05]
    
    df_platforms = pd.DataFrame({
        'platform': platforms,
        'percentage': platform_pct,
        'streams': [int(total_streams * p) for p in platform_pct]
    })
    
    return df_platforms

def generate_geographic_data(total_streams):
    """Generate geographic distribution data."""
    countries = ['United States', 'United Kingdom', 'Germany', 'Canada', 'Australia', 
                'France', 'Brazil', 'Mexico', 'Japan', 'Other']
    country_pct = [0.35, 0.15, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.07]
    
    df_geo = pd.DataFrame({
        'country': countries,
        'percentage': country_pct,
        'listeners': [int(total_streams * p) for p in country_pct]
    })
    
    return df_geo

def generate_demographic_data():
    """Generate demographic data (age and gender)."""
    # Age demographics
    age_groups = ['13-17', '18-24', '25-34', '35-44', '45-54', '55+']
    age_pct = [0.12, 0.35, 0.28, 0.15, 0.07, 0.03]
    
    df_age = pd.DataFrame({
        'age_group': age_groups,
        'percentage': age_pct
    })
    
    # Gender demographics
    gender = ['Female', 'Male', 'Non-binary/Other']
    gender_pct = [0.58, 0.40, 0.02]
    
    df_gender = pd.DataFrame({
        'gender': gender,
        'percentage': gender_pct
    })
    
    return df_age, df_gender

def generate_song_data(total_streams):
    """Generate sample data for top songs."""
    songs = ['Eternal Echoes', 'Midnight Dreams', 'Solar Flare', 
            'Ocean Waves', 'Mountain Peak']
    song_pct = [0.30, 0.25, 0.20, 0.15, 0.10]
    
    song_streams = [int(total_streams * p) for p in song_pct]
    
    df_songs = pd.DataFrame({
        'song': songs,
        'streams': song_streams,
        'avg_completion_rate': [random.uniform(0.7, 0.95) for _ in range(len(songs))],
        'saves': [int(s * random.uniform(0.1, 0.3)) for s in song_streams],
        'shares': [int(s * random.uniform(0.01, 0.05)) for s in song_streams]
    })
    
    return df_songs

def generate_song_daily_data(song_name, song_ratio, streaming_data):
    """Generate daily data for a specific song."""
    days = len(streaming_data)
    dates = streaming_data['date'].tolist()
    
    # Generate daily streams with some randomness
    daily_streams = []
    
    for i in range(days):
        # Weekend boost
        date = dates[i]
        weekend_boost = 1.3 if date.weekday() >= 5 else 1.0
        # Random fluctuation
        fluctuation = random.uniform(0.8, 1.2)
        # Calculate daily streams
        stream_count = int(streaming_data['streams'][i] * song_ratio * weekend_boost * fluctuation)
        daily_streams.append(stream_count)
    
    song_daily_data = pd.DataFrame({
        'date': dates,
        'streams': daily_streams,
        'song': song_name
    })
    
    return song_daily_data

def generate_revenue_data(platform_data):
    """Generate revenue data based on platform distribution."""
    # Sample revenue rates per stream for different platforms
    revenue_rates = {
        'Spotify': 0.00437,
        'Apple Music': 0.00735,
        'YouTube Music': 0.00069,
        'Amazon Music': 0.00402,
        'Other': 0.00250
    }
    
    revenue_data = platform_data.copy()
    revenue_data['revenue_per_stream'] = revenue_data['platform'].map(revenue_rates)
    revenue_data['total_revenue'] = revenue_data['streams'] * revenue_data['revenue_per_stream']
    
    return revenue_data

def generate_daily_revenue(streaming_data, revenue_data):
    """Generate daily revenue data."""
    daily_revenue = []
    
    for stream_count in streaming_data['streams']:
        # Calculate daily revenue based on platform distribution
        day_revenue = 0
        for i, platform in enumerate(revenue_data['platform']):
            platform_ratio = revenue_data['streams'][i] / revenue_data['streams'].sum()
            platform_streams = stream_count * platform_ratio
            platform_revenue = platform_streams * revenue_data['revenue_per_stream'][i]
            day_revenue += platform_revenue
        daily_revenue.append(day_revenue)
    
    revenue_trend = pd.DataFrame({
        'date': streaming_data['date'],
        'revenue': daily_revenue
    })
    
    return revenue_trend

def generate_revenue_projection(monthly_revenue, months=4):
    """Generate revenue projections for future months."""
    month_labels = ["Current Month"]
    month_labels.extend([f"Month {i+1}" for i in range(months-1)])
    
    # Growth rates for future months (e.g., 7%, 15%, 25% growth)
    growth_rates = [1.0]
    growth_rates.extend([1.0 + (0.07 * i) for i in range(1, months)])
    
    projected_revenue = [monthly_revenue * rate for rate in growth_rates]
    
    projection_df = pd.DataFrame({
        'month': month_labels,
        'projected_revenue': projected_revenue,
        'growth_rate': growth_rates
    })
    
    return projection_df

def get_all_sample_data(days=30):
    """Generate all sample data sets."""
    # Generate streaming data
    streaming_data = generate_streaming_data(days)
    total_streams = streaming_data['streams'].sum()
    
    # Generate platform data
    platform_data = generate_platform_data(total_streams)
    
    # Generate geographic data
    geo_data = generate_geographic_data(total_streams)
    
    # Generate demographic data
    age_data, gender_data = generate_demographic_data()
    
    # Generate song data
    song_data = generate_song_data(total_streams)
    
    # Generate revenue data
    revenue_data = generate_revenue_data(platform_data)
    daily_revenue = generate_daily_revenue(streaming_data, revenue_data)
    revenue_projection = generate_revenue_projection(daily_revenue['revenue'].sum())
    
    return {
        'streaming_data': streaming_data,
        'platform_data': platform_data,
        'geo_data': geo_data,
        'age_data': age_data,
        'gender_data': gender_data,
        'song_data': song_data,
        'revenue_data': revenue_data,
        'daily_revenue': daily_revenue,
        'revenue_projection': revenue_projection
    }

# Function to get song-specific daily data
def get_song_daily_data(song_name, song_data, streaming_data):
    """Get daily data for a specific song."""
    song_row = song_data[song_data['song'] == song_name]
    if len(song_row) == 0:
        return None
    
    song_ratio = song_row['streams'].iloc[0] / song_data['streams'].sum()
    return generate_song_daily_data(song_name, song_ratio, streaming_data)