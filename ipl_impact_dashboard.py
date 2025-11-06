import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="IPL Player Impact Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏏 IPL Player Impact Analysis")
st.markdown("""
**Revolutionizing cricket analytics with Win Probability Added (WPA)**  
*Discover which players actually change game outcomes, not just accumulate stats*
""")

# Load data - using only CSV files for deployment
@st.cache_data
def load_data():
    # Load top players from CSV
    top_batters = pd.read_csv('top_ipl_batters_by_wpa.csv', index_col=0)
    top_bowlers = pd.read_csv('top_ipl_bowlers_by_wpa.csv', index_col=0)
    
    return top_batters, top_bowlers

top_batters, top_bowlers = load_data()

# Sidebar
st.sidebar.header("🔍 Analysis Options")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis",
    ["Player Impact Rankings", "Methodology & Insights"]
)

# Main content based on selection
if analysis_type == "Player Impact Rankings":
    
    st.header("🎯 Most Impactful IPL Players")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏏 Top 10 Batters by Total Impact")
        # Sort descending for proper chart order (highest at top)
        top_batters_sorted = top_batters.head(10).sort_values('wpa', ascending=True)
        fig_batters = px.bar(
            top_batters_sorted,
            x='wpa',
            y=top_batters_sorted.index,
            orientation='h',
            color='wpa',
            color_continuous_scale='viridis',
            title='Total Win Probability Added'
        )
        fig_batters.update_layout(
            yaxis_title='Batter', 
            xaxis_title='Total WPA',
            showlegend=False
        )
        st.plotly_chart(fig_batters, use_container_width=True)
        
        # Key insights
        st.info("""
        **Key Insights:**
        - S Dhawan leads with +32.0 WPA (7,072 runs)
        - Traditional stars like V Kohli rank lower in impact
        - Context matters more than raw runs
        """)
    
    with col2:
        st.subheader("🎯 Top 10 Bowlers by Total Impact")
        # Sort descending for proper chart order (highest at top)
        top_bowlers_sorted = top_bowlers.head(10).sort_values('wpa', ascending=True)
        fig_bowlers = px.bar(
            top_bowlers_sorted,
            x='wpa',
            y=top_bowlers_sorted.index,
            orientation='h',
            color='wpa',
            color_continuous_scale='plasma',
            title='Total Win Probability Added'
        )
        fig_bowlers.update_layout(
            yaxis_title='Bowler', 
            xaxis_title='Total WPA',
            showlegend=False
        )
        st.plotly_chart(fig_bowlers, use_container_width=True)
        
        # Key insights
        st.info("""
        **Key Insights:**
        - YS Chahal dominates with +22.9 WPA
        - Wicket-taking isn't everything (see efficiency rankings)
        - Pressure bowling creates more impact
        """)
    
    # Efficiency rankings
    st.subheader("⚡ Most Efficient Players (Impact per 100 balls)")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Batters efficiency
        batters_efficiency = top_batters.nlargest(10, 'wpa_per_100_balls').sort_values('wpa_per_100_balls', ascending=True)
        fig_eff_bat = px.bar(
            batters_efficiency,
            x='wpa_per_100_balls',
            y=batters_efficiency.index,
            orientation='h',
            title='Batters: WPA per 100 balls',
            color='wpa_per_100_balls',
            color_continuous_scale='tealrose'
        )
        fig_eff_bat.update_layout(showlegend=False)
        st.plotly_chart(fig_eff_bat, use_container_width=True)
    
    with col4:
        # Bowlers efficiency
        bowlers_efficiency = top_bowlers.nlargest(10, 'wpa_per_100_balls').sort_values('wpa_per_100_balls', ascending=True)
        fig_eff_bowl = px.bar(
            bowlers_efficiency,
            x='wpa_per_100_balls',
            y=bowlers_efficiency.index,
            orientation='h',
            title='Bowlers: WPA per 100 balls',
            color='wpa_per_100_balls',
            color_continuous_scale='tealrose'
        )
        fig_eff_bowl.update_layout(showlegend=False)
        st.plotly_chart(fig_eff_bowl, use_container_width=True)
    
    # Show full tables
    st.subheader("📊 Complete Player Rankings")
    
    tab1, tab2 = st.tabs(["Batters", "Bowlers"])
    
    with tab1:
        st.dataframe(top_batters.round(3))
    
    with tab2:
        st.dataframe(top_bowlers.round(3))

else:  # Methodology & Insights
    
    st.header("🔬 Methodology & Key Insights")
    
    st.markdown("""
    ## 🎯 What is Win Probability Added (WPA)?
    
    **WPA measures how much each player's actions change their team's chance of winning.**
    
    ### Traditional Stats vs WPA:
    - **Runs scored**: Doesn't consider match situation
    - **Wickets taken**: Doesn't account for pressure moments  
    - **WPA**: Measures actual impact on game outcomes
    
    ### Revolutionary Findings:
    
    #### 1. **Weak Correlation with Traditional Stats**
    ```
    Runs vs WPA correlation: 0.113 (very weak)
    Wickets vs WPA correlation: -0.201 (slightly negative!)
    ```
    
    #### 2. **Hidden Gems Discovered**
    - **TH David**: Highest impact efficiency (+1.867 WPA/100 balls)
    - **R Tewatia**: Clutch performer (+0.933 WPA/100 balls) 
    - **LH Ferguson**: Most efficient bowler (+0.890 WPA/100 balls)
    
    #### 3. **Context Matters More Than Numbers**
    - A six in a pressure situation > multiple boundaries in dead rubber
    - A wicket when team is cruising < containing runs in tight chase
    
    ### 📊 Data Foundation:
    - **1,169 IPL matches** analyzed
    - **278,205 deliveries** processed  
    - **17 years** of historical data (2008-2024)
    - **Win probability model** trained on historical outcomes
    
    ### 🚀 Technical Implementation:
    - **Python** for data processing and analysis
    - **Pandas & SQLAlchemy** for data manipulation
    - **Plotly** for interactive visualizations
    - **Streamlit** for dashboard deployment
    """)
    
    # Correlation visualization
    st.subheader("📉 Traditional Stats vs Actual Impact")
    
    correlation_data = pd.DataFrame({
        'Metric': ['Runs vs WPA', 'Wickets vs WPA'],
        'Correlation': [0.113, -0.201]
    })
    
    fig_corr = px.bar(
        correlation_data,
        x='Metric',
        y='Correlation',
        color='Correlation',
        color_continuous_scale='rdylgn',
        title='Weak Correlation: Traditional Stats ≠ Game Impact'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Project story
    st.subheader("📖 Project Journey")
    st.markdown("""
    This project represents a comprehensive sports analytics pipeline:
    
    1. **Data Collection**: 1,169 IPL matches from Cricsheet
    2. **Data Processing**: Built SQL database with 278,205 deliveries
    3. **Model Development**: Created win probability model using historical frequencies
    4. **Analysis**: Calculated Win Probability Added for every player
    5. **Visualization**: Built interactive dashboard to showcase insights
    
    The results challenge conventional cricket wisdom and provide new ways to evaluate player performance.
    """)

# Footer
st.markdown("---")
st.markdown("""
**Built with Python • Data from Cricsheet • Win Probability Model by Burt Louw**  
*Connect with me on LinkedIn to discuss sports analytics!*
""")