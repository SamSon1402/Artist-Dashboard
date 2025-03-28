import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Define color schemes
COLOR_SCHEMES = {
    'primary': ['#6e45e2', '#7149EA', '#9067ff', '#BD4DE6'],
    'success': ['#4caf50', '#2e7d32'],
    'neutral': ['#151530', '#201a4a', '#2c2c4a', '#3D3D3D'],
    'text': ['#ffffff', '#e0e0ff', '#c9b6ff']
}

def create_line_chart(data, x, y, title=None, color=None, use_markers=False):
    """Create a line chart with consistent styling."""
    fig = px.line(data, x=x, y=y, markers=use_markers, color=color)
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x.capitalize() if isinstance(x, str) else None,
        yaxis_title=y.capitalize() if isinstance(y, str) else None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        )
    )
    
    # Update line and marker colors if no color is specified
    if color is None:
        fig.update_traces(
            line=dict(color=COLOR_SCHEMES['primary'][0], width=3),
            marker=dict(color=COLOR_SCHEMES['primary'][1], size=8) if use_markers else None
        )
    
    return fig

def create_bar_chart(data, x, y, title=None, color=None, color_scale=None, text=None, horizontal=False):
    """Create a bar chart with consistent styling."""
    if horizontal:
        fig = px.bar(data, y=x, x=y, color=color, color_continuous_scale=color_scale, text=text)
    else:
        fig = px.bar(data, x=x, y=y, color=color, color_continuous_scale=color_scale, text=text)
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x.capitalize() if isinstance(x, str) else None,
        yaxis_title=y.capitalize() if isinstance(y, str) else None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        )
    )
    
    # If no color is specified, use primary color
    if color is None and color_scale is None:
        fig.update_traces(marker_color=COLOR_SCHEMES['primary'][0])
    
    return fig

def create_pie_chart(data, values, names, title=None, hole=0.4):
    """Create a pie chart with consistent styling."""
    fig = px.pie(data, values=values, names=names, hole=hole)
    
    # Update layout
    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # Update colors to use a consistent color palette
    fig.update_traces(
        marker=dict(colors=COLOR_SCHEMES['primary']),
        textfont_color='#ffffff'
    )
    
    return fig

def create_heatmap(data, x, y, z, title=None, color_scale=None):
    """Create a heatmap with consistent styling."""
    if color_scale is None:
        color_scale = [[0, "#151530"], [1, "#6e45e2"]]
    
    fig = px.imshow(
        data,
        x=x if isinstance(x, list) else data[x].tolist(),
        y=y if isinstance(y, list) else data[y].tolist(),
        z=z if isinstance(z, list) else data[z].tolist(),
        color_continuous_scale=color_scale
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x if isinstance(x, str) else None,
        yaxis_title=y if isinstance(y, str) else None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff'
    )
    
    return fig

def create_group_bar_chart(data, x, y_values, names, title=None):
    """Create a grouped bar chart for comparing multiple series."""
    fig = go.Figure()
    
    colors = COLOR_SCHEMES['primary']
    
    for i, y in enumerate(y_values):
        fig.add_trace(go.Bar(
            x=data[x],
            y=data[y],
            name=names[i],
            marker_color=colors[i % len(colors)]
        ))
    
    # Update layout
    fig.update_layout(
        title=title,
        barmode='group',
        xaxis_title=x.capitalize() if isinstance(x, str) else None,
        yaxis_title="Value",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff'
    )
    
    return fig

def create_area_chart(data, x, y, title=None, color=None):
    """Create an area chart with consistent styling."""
    fig = px.area(data, x=x, y=y, color=color)
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x.capitalize() if isinstance(x, str) else None,
        yaxis_title=y.capitalize() if isinstance(y, str) else None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0ff',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.15)'
        )
    )
    
    if color is None:
        fig.update_traces(
            line=dict(color=COLOR_SCHEMES['primary'][0]),
            fillcolor=COLOR_SCHEMES['primary'][0],
            opacity=0.3
        )
    
    return fig