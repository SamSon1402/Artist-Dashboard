import streamlit as st
import pandas as pd
import plotly.express as px
from data.sample_data import get_all_sample_data, get_song_daily_data
from utils.visualization import create_line_chart, create_bar_chart

def show(time_period):
    """Display the content performance page."""
    st.title("Content Performance")
    
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
    song_data = data['song_data']
    
    # Top songs table
    st.subheader("Top Songs")
    
    # Format the song data for display
    formatted_song_data = song_data.copy()
    
    # Convert to percentage for display
    formatted_song_data['avg_completion_rate'] = formatted_song_data['avg_completion_rate'] * 100
    
    # Display as a table
    st.dataframe(
        formatted_song_data.style.format({
            'streams': '{:,}',
            'avg_completion_rate': '{:.1f}%',
            'saves': '{:,}',
            'shares': '{:,}'
        }),
        use_container_width=True
    )
    
    # Song performance metrics
    st.subheader("Song Performance Metrics")
    
    # Select a song to analyze
    song_select = st.selectbox("Select Song", song_data['song'])
    
    # Get the selected song's data
    selected_index = song_data[song_data['song'] == song_select].index[0]
    
    # Display key metrics for the selected song
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Streams", 
            f"{song_data.loc[selected_index, 'streams']:,}", 
            "+12.4%"
        )
    
    with col2:
        completion_rate = song_data.loc[selected_index, 'avg_completion_rate'] * 100
        st.metric(
            "Avg. Completion Rate", 
            f"{completion_rate:.1f}%", 
            "+2.3%"
        )
    
    with col3:
        st.metric(
            "Saves", 
            f"{song_data.loc[selected_index, 'saves']:,}", 
            "+18.7%"
        )
    
    with col4:
        st.metric(
            "Shares", 
            f"{song_data.loc[selected_index, 'shares']:,}", 
            "+7.9%"
        )
    
    # Get daily performance for the selected song
    song_daily_data = get_song_daily_data(song_select, song_data, streaming_data)
    
    # Display daily performance chart
    st.subheader(f"Daily Performance: {song_select}")
    
    fig = create_line_chart(
        song_daily_data,
        x='date',
        y='streams',
        title=f"Daily Streams: {song_select}",
        use_markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform performance
    st.subheader("Platform Breakdown")
    
    # Create sample platform breakdown for the selected song
    platforms = ['Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 'Other']
    
    # Generate random distribution that sums to the total streams
    total_song_streams = song_data.loc[selected_index, 'streams']
    
    # Base percentages with some randomness
    platform_pct = [0.45, 0.25, 0.15, 0.10, 0.05]
    platform_streams = [int(total_song_streams * p) for p in platform_pct]
    
    platform_data = pd.DataFrame({
        'platform': platforms,
        'streams': platform_streams
    })
    
    fig = create_bar_chart(
        platform_data,
        x='platform',
        y='streams',
        title=f"Platform Breakdown: {song_select}",
        color_scale='viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Content comparison
    st.subheader("Song Comparison")
    
    # Select songs to compare
    compare_songs = st.multiselect(
        "Select Songs to Compare",
        song_data['song'].tolist(),
        default=[song_data['song'].iloc[0], song_data['song'].iloc[1]]
    )
    
    if compare_songs:
        # Select metrics to compare
        metrics = st.multiselect(
            "Select Metrics",
            ["Streams", "Avg. Completion Rate", "Saves", "Shares"],
            default=["Streams", "Avg. Completion Rate"]
        )
        
        if metrics:
            # Create comparison data
            comparison_data = song_data[song_data['song'].isin(compare_songs)].copy()
            
            # Convert completion rate to percentage for display
            comparison_data['avg_completion_rate'] = comparison_data['avg_completion_rate'] * 100
            
            # Create separate charts for each selected metric
            for metric in metrics:
                if metric == "Streams":
                    y_col = 'streams'
                    format_str = '{:,}'
                elif metric == "Avg. Completion Rate":
                    y_col = 'avg_completion_rate'
                    format_str = '{:.1f}%'
                elif metric == "Saves":
                    y_col = 'saves'
                    format_str = '{:,}'
                else:  # Shares
                    y_col = 'shares'
                    format_str = '{:,}'
                
                fig = create_bar_chart(
                    comparison_data,
                    x='song',
                    y=y_col,
                    title=f"Comparison by {metric}",
                    color_scale='viridis'
                )
                st.plotly_chart(fig, use_container_width=True)