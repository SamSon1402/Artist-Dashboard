import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.sample_data import get_all_sample_data
from utils.visualization import create_line_chart, create_bar_chart, create_group_bar_chart

def show(time_period):
    """Display the revenue analytics page."""
    st.title("Revenue Analytics")
    
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
    revenue_data = data['revenue_data']
    daily_revenue = data['daily_revenue']
    revenue_projection = data['revenue_projection']
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_revenue = revenue_data['total_revenue'].sum()
        st.metric(
            "Total Revenue", 
            f"${total_revenue:.2f}", 
            "+11.3%"
        )
    
    with col2:
        avg_daily_revenue = total_revenue / days
        st.metric(
            "Avg. Daily Revenue", 
            f"${avg_daily_revenue:.2f}", 
            "+8.7%"
        )
    
    with col3:
        total_streams = revenue_data['streams'].sum()
        avg_per_stream = total_revenue / total_streams
        st.metric(
            "Avg. Revenue per Stream", 
            f"${avg_per_stream:.5f}", 
            "+2.1%"
        )
    
    st.markdown("---")
    
    # Revenue by platform
    st.subheader("Revenue by Platform")
    
    fig = create_bar_chart(
        revenue_data,
        x='platform',
        y='total_revenue',
        title="Revenue by Platform",
        color_scale='viridis',
        text=[f"${v:.2f}" for v in revenue_data['total_revenue']]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Streams vs Revenue comparison
    st.subheader("Streams vs Revenue by Platform")
    
    # Create a grouped bar chart with streams and revenue
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=revenue_data['platform'],
        y=revenue_data['streams'],
        name='Streams',
        marker_color='#6e45e2'
    ))
    
    fig.add_trace(go.Bar(
        x=revenue_data['platform'],
        y=revenue_data['total_revenue'],
        name='Revenue ($)',
        marker_color='#BD4DE6'
    ))
    
    fig.update_layout(
        title="Streams vs Revenue by Platform",
        barmode='group',
        xaxis_title="Platform",
        yaxis_title="Count",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue trend
    st.subheader(f"Revenue Trend ({time_period})")
    
    fig = create_line_chart(
        daily_revenue,
        x='date',
        y='revenue',
        title=f"Daily Revenue ({time_period})",
        use_markers=True
    )
    fig.update_traces(
        name="Revenue",
        hovertemplate="Date: %{x}<br>Revenue: $%{y:.2f}"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly revenue analysis
    st.subheader("Weekly Revenue Analysis")
    
    # Convert to weekly format
    daily_revenue['week'] = daily_revenue['date'].dt.isocalendar().week
    weekly_revenue = daily_revenue.groupby('week').agg({
        'revenue': 'sum',
        'date': 'first'  # Take the first day of each week for the x-axis
    }).reset_index()
    
    fig = create_bar_chart(
        weekly_revenue,
        x='date',
        y='revenue',
        title="Weekly Revenue",
        color_scale='viridis',
        text=[f"${v:.2f}" for v in weekly_revenue['revenue']]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue projection
    st.subheader("Revenue Projection")
    
    fig = create_bar_chart(
        revenue_projection, 
        x='month', 
        y='projected_revenue',
        title="Revenue Projection",
        color_scale='viridis',
        text=[f"${v:.2f}" for v in revenue_projection['projected_revenue']]
    )
    
    # Add growth rate as text above bars
    for i, row in enumerate(revenue_projection.itertuples()):
        if i > 0:  # Skip the first month (no growth)
            growth_pct = (row.growth_rate - 1) * 100
            fig.add_annotation(
                x=row.month,
                y=row.projected_revenue + 10,
                text=f"+{growth_pct:.1f}%",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=12,
                    color="#4caf50"
                )
            )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue per stream analysis
    st.subheader("Revenue per Stream Analysis")
    
    # Display rates by platform
    revenue_rates = revenue_data[['platform', 'revenue_per_stream']].copy()
    
    st.write("Revenue Rates by Platform")
    st.dataframe(
        revenue_rates.style.format({
            'revenue_per_stream': '${:.5f}'
        }),
        use_container_width=True
    )
    
    # Create a bar chart of revenue rates
    fig = create_bar_chart(
        revenue_rates,
        x='platform',
        y='revenue_per_stream',
        title="Revenue per Stream by Platform",
        color_scale='viridis',
        text=[f"${v:.5f}" for v in revenue_rates['revenue_per_stream']]
    )
    st.plotly_chart(fig, use_container_width=True)