import streamlit as st
import pandas as pd
import plotly.express as px
import random
from data.sample_data import get_all_sample_data
from utils.visualization import create_pie_chart, create_bar_chart, create_heatmap

def show(time_period):
    """Display the audience insights page."""
    st.title("Audience Insights")
    
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
    geo_data = data['geo_data']
    age_data = data['age_data']
    gender_data = data['gender_data']
    
    # Geographic distribution
    st.subheader("Geographic Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_pie_chart(
            geo_data,
            values='listeners',
            names='country',
            title="Listeners by Country"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_bar_chart(
            geo_data.sort_values('listeners', ascending=False),
            x='country',
            y='listeners',
            title="Listeners by Country",
            color_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Age and gender distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Age Demographics")
        fig = create_bar_chart(
            age_data,
            x='age_group',
            y='percentage',
            title="Listeners by Age Group",
            color_scale='viridis',
            text=[f"{p:.1%}" for p in age_data['percentage']]
        )
        fig.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Gender Distribution")
        fig = create_pie_chart(
            gender_data,
            values='percentage',
            names='gender',
            title="Listeners by Gender"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Audience growth trends
    st.subheader("Audience Growth by Region")
    
    # Create sample region growth data
    regions = geo_data['country'].tolist()[:5]  # Top 5 countries
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    growth_data = pd.DataFrame()
    
    for region in regions:
        # Generate growth percentages with some randomness
        base = geo_data[geo_data['country'] == region]['percentage'].iloc[0]
        growth = [base]
        for i in range(1, len(months)):
            # Add a growth trend between 2-10%
            growth.append(growth[i-1] * (1 + (0.02 + random.random() * 0.08)))
        
        # Add to dataframe
        region_df = pd.DataFrame({
            'month': months,
            'region': region,
            'growth': growth
        })
        growth_data = pd.concat([growth_data, region_df], ignore_index=True)
    
    fig = px.line(
        growth_data,
        x='month',
        y='growth',
        color='region',
        title="Audience Growth by Region",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Audience Share",
        yaxis_tickformat='.1%',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        legend_title="Region"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Engagement metrics
    st.subheader("Engagement Metrics by Demographics")
    
    # Create sample engagement metrics
    metrics = ["Stream Completion", "Save Rate", "Share Rate", "Repeat Listens"]
    age_groups = age_data['age_group'].tolist()
    
    engagement_data = pd.DataFrame()
    
    for age in age_groups:
        metric_values = []
        for _ in range(len(metrics)):
            # Generate random engagement metrics between 10-90%
            metric_values.append(0.1 + (random.random() * 0.8))
        
        age_df = pd.DataFrame({
            'age_group': [age] * len(metrics),
            'metric': metrics,
            'value': metric_values
        })
        engagement_data = pd.concat([engagement_data, age_df], ignore_index=True)
    
    # Create a pivot table for the heatmap
    pivot_data = engagement_data.pivot(index='metric', columns='age_group', values='value')
    
    # Create heatmap
    fig = px.imshow(
        pivot_data,
        text_auto='.0%',
        color_continuous_scale='viridis',
        title="Engagement Metrics by Age Group"
    )
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Metric",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform preference by demographic
    st.subheader("Platform Preference by Age Group")
    
    # Create sample platform preference data
    platforms = ['Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 'Other']
    
    platform_pref_data = pd.DataFrame()
    
    for age in age_groups:
        platform_values = []
        # Generate random platform preferences that sum to 1
        raw_values = [random.random() for _ in range(len(platforms))]
        sum_values = sum(raw_values)
        norm_values = [v / sum_values for v in raw_values]
        
        age_df = pd.DataFrame({
            'age_group': [age] * len(platforms),
            'platform': platforms,
            'percentage': norm_values
        })
        platform_pref_data = pd.concat([platform_pref_data, age_df], ignore_index=True)
    
    # Create bar chart
    fig = px.bar(
        platform_pref_data,
        x='age_group',
        y='percentage',
        color='platform',
        title="Platform Preference by Age Group",
        barmode='stack',
        text_auto='.0%'
    )
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Percentage",
        yaxis_tickformat='.0%',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        legend_title="Platform"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Listening time analysis
    st.subheader("Listening Time Analysis")
    
    # Create sample listening time data
    hours = list(range(24))
    hour_labels = [f"{h}:00" for h in hours]
    
    listening_data = pd.DataFrame()
    
    # Generate random listening patterns for different age groups
    for age in age_groups[:3]:  # Use first 3 age groups to avoid cluttering
        listening_values = []
        
        if age == '13-17':
            # Teens: more evening and night listening
            for h in hours:
                if 15 <= h <= 23:  # 3 PM to 11 PM peak
                    listening_values.append(0.5 + random.random() * 0.5)
                else:
                    listening_values.append(random.random() * 0.5)
        elif age == '18-24':
            # Young adults: late night preference
            for h in hours:
                if 20 <= h or h <= 2:  # 8 PM to 2 AM peak
                    listening_values.append(0.5 + random.random() * 0.5)
                else:
                    listening_values.append(random.random() * 0.5)
        else:  # 25-34
            # Adults: morning and evening commute
            for h in hours:
                if 7 <= h <= 9 or 16 <= h <= 19:  # 7-9 AM and 4-7 PM peaks
                    listening_values.append(0.5 + random.random() * 0.5)
                else:
                    listening_values.append(random.random() * 0.5)
        
        # Normalize values
        max_value = max(listening_values)
        norm_values = [v / max_value for v in listening_values]
        
        age_df = pd.DataFrame({
            'hour': hour_labels,
            'age_group': age,
            'listening_activity': norm_values
        })
        listening_data = pd.concat([listening_data, age_df], ignore_index=True)
    
    # Create line chart
    fig = px.line(
        listening_data,
        x='hour',
        y='listening_activity',
        color='age_group',
        title="Listening Activity by Hour of Day",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Relative Listening Activity",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        legend_title="Age Group",
        xaxis=dict(
            tickmode='array',
            tickvals=hour_labels[::2],  # Show every other hour for clarity
            ticktext=hour_labels[::2]
        )
    )
    st.plotly_chart(fig, use_container_width=True)