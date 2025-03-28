import streamlit as st
from pages import overview, audience, content, revenue

# Set page configuration
st.set_page_config(
    page_title="Artist Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
def load_css():
    with open("assets/css/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Try to load CSS, create file if it doesn't exist
try:
    load_css()
except FileNotFoundError:
    import os
    if not os.path.exists("assets/css"):
        os.makedirs("assets/css")
    with open("assets/css/style.css", "w") as f:
        f.write("""
        /* Custom CSS for Artist Dashboard */
        .sidebar .sidebar-content {
            background-color: #1E1E1E;
        }
        .metric-card {
            border: 1px solid #3D3D3D;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .stButton>button {
            width: 100%;
        }
        """)
    load_css()

# Sidebar
def sidebar():
    try:
        st.sidebar.image("assets/images/logo.png", width=150)
    except:
        st.sidebar.title("Artist Dashboard")
    
    st.sidebar.markdown("---")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigate", ["Overview", "Audience", "Content", "Revenue"])
    
    st.sidebar.markdown("---")
    
    # Time period selector
    time_period = st.sidebar.selectbox(
        "Time Period",
        ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"]
    )
    
    st.sidebar.markdown("---")
    
    # Settings section
    with st.sidebar.expander("Settings"):
        data_source = st.selectbox(
            "Data Source",
            ["Sample Data", "Spotify", "Apple Music", "YouTube Music", "All Platforms"]
        )
        
        refresh_data = st.button("Refresh Data")
        
        if refresh_data:
            st.sidebar.success("Data refreshed successfully!")
    
    st.sidebar.markdown("---")
    st.sidebar.info("This is a demo dashboard. Connect to real streaming platforms for actual data.")
    
    return page, time_period

# Main function
def main():
    page, time_period = sidebar()
    
    # Display the appropriate page based on navigation
    if page == "Overview":
        overview.show(time_period)
    elif page == "Audience":
        audience.show(time_period)
    elif page == "Content":
        content.show(time_period)
    elif page == "Revenue":
        revenue.show(time_period)
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 Artist Dashboard | Created with Streamlit")

if __name__ == "__main__":
    main()