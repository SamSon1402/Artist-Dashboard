# Artist Dashboard

A comprehensive analytics dashboard for musicians and artists to track streaming performance, audience demographics, content metrics, and revenue data.

![Image](https://github.com/user-attachments/assets/fd273ef0-844f-45ab-a3eb-696c554e6708)
![Image](https://github.com/user-attachments/assets/88f42fb0-55e4-4c07-8424-006507ae440c)
![Image](https://github.com/user-attachments/assets/b076fad1-f11b-4689-8b99-9a04856544ca)
![Image](https://github.com/user-attachments/assets/af1696b2-8daf-4fa6-a047-7c1ec743f94c)

## Features

- **Overview Dashboard**: Track key metrics, streaming trends, follower growth, platform distribution, and top songs
- **Audience Insights**: Analyze geographic distribution, age/gender demographics, and engagement patterns
- **Content Performance**: Monitor individual song performance with detailed metrics and comparisons
- **Revenue Analytics**: Track revenue by platform, analyze trends, and view projections

## Technologies

- **Streamlit**: Powers the interactive web interface
- **Plotly**: Creates dynamic, interactive visualizations
- **Pandas**: Handles data processing and analysis
- **Python 3.9+**: Core programming language

## Project Structure

```
artist-dashboard/
│
├── app.py                      # Main application entry point
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore file
│
├── assets/                     # Static assets
│   ├── css/                    # Custom CSS files
│   │   └── style.css           # Main stylesheet
│   └── images/                 # Images for the application
│       └── logo.png            # App logo
│
├── config/                     # Configuration files
│   ├── __init__.py             # Make directory a package
│   ├── config.py               # Configuration settings
│   └── credentials.py          # API keys and credentials (gitignored)
│
├── data/                       # Data storage and processing
│   ├── __init__.py             # Make directory a package
│   ├── sample_data.py          # Sample data generator
│   └── data_processor.py       # Data processing utilities
│
├── pages/                      # Streamlit pages
│   ├── __init__.py             # Make directory a package
│   ├── overview.py             # Overview dashboard page
│   ├── audience.py             # Audience insights page
│   ├── content.py              # Content performance page
│   └── revenue.py              # Revenue analytics page
│
├── services/                   # External API integrations
│   ├── __init__.py             # Make directory a package
│   ├── spotify_service.py      # Spotify API integration
│   ├── apple_music_service.py  # Apple Music API integration
│   ├── youtube_service.py      # YouTube Music API integration
│   └── amazon_service.py       # Amazon Music API integration
│
├── utils/                      # Utility functions
│   ├── __init__.py             # Make directory a package
│   ├── visualization.py        # Visualization helpers
│   ├── date_utils.py           # Date manipulation utilities
│   └── analytics.py            # Analytics computation utilities
│
└── models/                     # Data models
    ├── __init__.py             # Make directory a package
    └── streaming_data.py       # Data models for streaming information
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/artist-dashboard.git
cd artist-dashboard
```

2. Create and activate a virtual environment:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `config/credentials.py` file with your API keys:
```python
# Spotify API credentials
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"

# Apple Music API credentials
APPLE_MUSIC_KEY_ID = "your_apple_music_key_id"
APPLE_MUSIC_TEAM_ID = "your_apple_music_team_id"
APPLE_MUSIC_PRIVATE_KEY = "your_apple_music_private_key_path"

# YouTube Music API credentials
YOUTUBE_API_KEY = "your_youtube_api_key"

# Amazon Music API credentials
AMAZON_MUSIC_CLIENT_ID = "your_amazon_music_client_id"
AMAZON_MUSIC_CLIENT_SECRET = "your_amazon_music_client_secret"
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Use the sidebar to navigate between different dashboard sections

4. Select different time periods to view data for specific timeframes

## Sample Data Mode

By default, the dashboard uses sample data to demonstrate capabilities without requiring API credentials. To use real data:

1. Ensure you have valid API credentials in the `config/credentials.py` file
2. Select the appropriate data source in the Settings panel in the sidebar

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python -m unittest discover tests`
5. Submit a pull request

## API Integrations

The dashboard integrates with multiple music streaming platforms:

- **Spotify**: Artist data, tracks, and basic metrics
- **Apple Music**: Song and album information
- **YouTube Music**: Video performance and channel statistics
- **Amazon Music**: Limited integration (placeholder only)

Note that full streaming performance data requires artist account access and proper authentication.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Sample data structure inspired by music industry standards
