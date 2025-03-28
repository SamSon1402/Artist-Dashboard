"""Configuration settings for the Artist Dashboard application."""

# Application settings
APP_NAME = "Artist Dashboard"
APP_VERSION = "1.0.0"
THEME_COLOR = "#6e45e2"

# Data settings
DEFAULT_DAYS = 30
DEFAULT_PLATFORM = "Sample Data"

# API settings
API_TIMEOUT = 30  # seconds
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Chart settings
DEFAULT_CHART_HEIGHT = 400
COLOR_SCHEMES = {
    'primary': ['#6e45e2', '#7149EA', '#9067ff', '#BD4DE6'],
    'success': ['#4caf50', '#2e7d32'],
    'neutral': ['#151530', '#201a4a', '#2c2c4a', '#3D3D3D'],
    'text': ['#ffffff', '#e0e0ff', '#c9b6ff']
}