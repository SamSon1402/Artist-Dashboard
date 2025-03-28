import streamlit as st
import plotly.express as px
import pandas as pd
from data.sample_data import get_all_sample_data
from utils.visualization import create_line_chart, create_pie_chart, create_bar_chart

def show(time_period):
    """Display the overview dashboard."""
    st.title("Overview Dashboard")
    
    # Determine days based on time period
    days = 30  # Default to 30 days
    if time_period == "Last 90 Days":
        days = 90
    elif time_period == "Last 6 Months":
        days = 180
    elif time_period == "Last Year":
        days = 365
    
    # Get sample data
    data = get_all_sample_data(days)
    streaming_data = data['streaming_data']
    platform_data = data['platform_data']
    song_data = data['song_data']
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_streams = streaming_data['streams'].sum()
        st.metric(
            "Total Streams", 
            f"{total_streams:,}", 
            "+15.3%"
        )
    
    with col2:
        current_followers = streaming_data['followers'].iloc[-1]
        follower_change = current_followers - streaming_data['followers'].iloc[0]
        follower_change_pct = (follower_change / streaming_data['followers'].iloc[0]) * 100
        
        st.metric(
            "Current Followers", 
            f"{current_followers:,}", 
            f"+{follower_change:,} ({follower_change_pct:.1f}%)"
        )
    
    with col3:
        avg_streams = int(streaming_data['streams'].mean())
        st.metric(
            "Avg. Daily Streams", 
            f"{avg_streams:,}", 
            "+7.2%"
        )
    
    with col4:
        platforms = len(platform_data) - 1  # Excluding "Other"
        st.metric(
            "Platforms", 
            platforms, 
            "+1"
        )
    
    st.markdown("---")
    
    # Stream and follower trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Daily Streams ({time_period})")
        fig = create_line_chart(
            streaming_data, 
            x='date', 
            y='streams',
            title=f"Daily Streams ({time_period})",
            use_markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Follower Growth")
        fig = create_line_chart(
            streaming_data, 
            x='date', 
            y='followers',
            title="Follower Growth"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Platform breakdown and top songs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Platform Distribution")
        fig = create_pie_chart(
            platform_data, 
            values='streams', 
            names='platform',
            title="Streams by Platform"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Songs")
        fig = create_bar_chart(
            song_data, 
            x='song', 
            y='streams',
            title="Streams by Song",
            color_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly analysis
    st.subheader("Weekly Performance Analysis")
    
    # Convert data to weekly format
    streaming_data['week'] = streaming_data['date'].dt.isocalendar().week
    weekly_data = streaming_data.groupby('week').agg({
        'streams': 'sum',
        'date': 'first'  # Take the first day of each week for the x-axis
    }).reset_index()
    
    fig = create_line_chart(
        weekly_data, 
        x='date', 
        y='streams',
        title="Weekly Streams",
        use_markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance by day of week
    st.subheader("Performance by Day of Week")
    
    # Add day of week column
    streaming_data['day_of_week'] = streaming_data['date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Group by day of week
    day_performance = streaming_data.groupby('day_of_week').agg({
        'streams': 'mean'
    }).reset_index()
    
    # Reorder days
    day_performance['day_of_week'] = pd.Categorical(
        day_performance['day_of_week'], 
        categories=day_order, 
        ordered=True
    )
    day_performance = day_performance.sort_values('day_of_week')
    
    fig = create_bar_chart(
        day_performance, 
        x='day_of_week', 
        y='streams',
        title="Average Streams by Day of Week",
        color_scale='viridis'
    )
    st.plotly_chart(fig, use_container_width=True)