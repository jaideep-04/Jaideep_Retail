import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime
import logging

st.set_page_config(
    page_title="Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

logger = logging.getLogger(__name__)
API_BASE_URL = "http://localhost:8000/api/v1"

# ============================================================================
# MODERN DARK THEME STYLING
# ============================================================================

MODERN_THEME = """
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [class*="css"] {
        background-color: #0f1419 !important;
        color: #e8eaed !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0f1419;
        color: #e8eaed;
    }
    
    [data-testid="stHeader"] {
        background-color: #0f1419;
        padding: 1rem 2rem;
        border-bottom: 1px solid #2d3748;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a2332;
        border-right: 1px solid #2d3748;
    }
    
    .stRadio > label > span {
        color: #e8eaed !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    .stRadio > label {
        padding: 8px 12px !important;
        border-radius: 4px !important;
        margin: 4px 0 !important;
        transition: all 0.2s !important;
    }
    
    .stRadio > label:hover {
        background-color: rgba(63, 81, 181, 0.15) !important;
    }
    
    .main-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 2rem 0 2.5rem 0;
        padding: 0 1rem;
    }
    
    .header-title {
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 13px;
        color: #90caf9;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-header {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        margin: 2.5rem 0 1.5rem 1rem;
        padding: 0;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 0 1rem 2rem 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a2332 0%, #232f3e 100%);
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border-top: 3px solid #3f51b5;
    }
    
    .metric-card:hover {
        background: linear-gradient(135deg, #232f3e 0%, #2a3f5f 100%);
        border-color: #3f51b5;
        box-shadow: 0 6px 20px rgba(63, 81, 181, 0.2);
    }
    
    .metric-card.metric-green {
        border-top-color: #4caf50;
    }
    
    .metric-card.metric-orange {
        border-top-color: #ff9800;
    }
    
    .metric-card.metric-purple {
        border-top-color: #9c27b0;
    }
    
    .metric-label {
        font-size: 11px;
        font-weight: 700;
        color: #90caf9;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        display: block;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        font-family: 'Monaco', 'Menlo', monospace;
    }
    
    .metric-change {
        font-size: 12px;
        color: #4caf50;
        font-weight: 600;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #1a2332 0%, #232f3e 100%);
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin: 1rem;
    }
    
    .chart-title {
        font-size: 14px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .data-table-container {
        background: linear-gradient(135deg, #1a2332 0%, #232f3e 100%);
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin: 1rem;
    }
    
    [data-testid="stDataFrame"] {
        color: #e8eaed !important;
    }
    
    [data-testid="stDataFrame"] > div > div > table {
        background-color: rgba(26, 35, 50, 0.5) !important;
    }
    
    [data-testid="stDataFrame"] > div > div > table tbody tr {
        background-color: rgba(26, 35, 50, 0.3) !important;
    }
    
    [data-testid="stDataFrame"] > div > div > table thead tr {
        background-color: rgba(63, 81, 181, 0.15) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3f51b5 0%, #2c3e9c 100%);
        color: white;
        border: 1px solid #5561d9;
        border-radius: 4px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 12px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(63, 81, 181, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5561d9 0%, #3f51b5 100%);
        box-shadow: 0 6px 20px rgba(63, 81, 181, 0.4);
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #1a2332 !important;
        color: #e8eaed !important;
        border: 1px solid #2d3748 !important;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 13px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3f51b5 !important;
        box-shadow: 0 0 0 2px rgba(63, 81, 181, 0.2) !important;
    }
    
    .nav-header {
        color: #ffffff;
        font-size: 16px;
        font-weight: 700;
        padding: 1.5rem 1rem 1rem 1rem;
        border-bottom: 1px solid #2d3748;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .info-box {
        background: rgba(63, 81, 181, 0.15);
        border-left: 4px solid #3f51b5;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 13px;
        color: #90caf9;
        font-weight: 500;
        margin: 12px 0;
    }
    
    .success-box {
        background: rgba(76, 175, 80, 0.15);
        border-left: 4px solid #4caf50;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 13px;
        color: #81c784;
        font-weight: 500;
        margin: 12px 0;
    }
    
    .warning-box {
        background: rgba(255, 152, 0, 0.15);
        border-left: 4px solid #ff9800;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 13px;
        color: #ffb74d;
        font-weight: 500;
        margin: 12px 0;
    }
    
    .timestamp {
        font-size: 11px;
        color: #78909c;
        text-align: right;
        margin-top: 1rem;
    }
</style>
"""

st.markdown(MODERN_THEME, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown('<div class="nav-header">Navigation</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Select View",
        ["Overview", "Revenue", "Products", "Customers", "Search"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 1rem; font-size: 11px; color: #78909c;">
    <strong>Last Updated</strong><br>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br><br>
    <strong>Status</strong><br><span style="color: #4caf50;">● Active</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# API FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def fetch_overview():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/overview", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def fetch_monthly_revenue():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/monthly-revenue", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def fetch_country_revenue():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/country-revenue?limit=15", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def fetch_top_products():
    try:
        response = requests.get(f"{API_BASE_URL}/transactions/stats/top-products?limit=15", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def fetch_top_customers():
    try:
        response = requests.get(f"{API_BASE_URL}/transactions/stats/top-customers?limit=10", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def search_products(query):
    try:
        response = requests.get(f"{API_BASE_URL}/products/search/{query}?limit=50", timeout=5)
        return response.json()["data"] if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def fetch_customer_by_country(country):
    try:
        response = requests.get(f"{API_BASE_URL}/customers/country/{country}", timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# ============================================================================
# METRIC CARD COMPONENT
# ============================================================================

def show_metric(col, label, value, change="", card_class=""):
    with col:
        st.markdown(f"""
        <div class="metric-card {card_class}">
            <span class="metric-label">{label}</span>
            <div class="metric-value">{value}</div>
            <span class="metric-change">{change}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

def page_overview():
    st.markdown('<h1 class="header-title">Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Real-time Business Intelligence</p>', unsafe_allow_html=True)
    
    overview = fetch_overview()
    if not overview:
        st.error("Unable to load dashboard data")
        return
    
    # KPI Metrics
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    show_metric(col1, "Total Revenue", f"£{overview['total_revenue']:,.0f}", "All time", "")
    show_metric(col2, "Total Orders", f"{overview['total_transactions']:,}", "Transactions", "metric-green")
    show_metric(col3, "Active Customers", f"{overview['total_customers']:,}", "Registered", "metric-orange")
    show_metric(col4, "Products", f"{overview['total_products']:,}", "Catalog", "metric-purple")
    
    # Charts Row - IMPROVED PRODUCT CHARTS
    st.markdown('<div class="section-header">Product Insights</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
    
    top_products = fetch_top_products()
    if top_products:
        products_df = pd.DataFrame(top_products[:10])
        products_df = products_df.sort_values('total_revenue', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=products_df['stock_code'],
            x=products_df['total_revenue'],
            orientation='h',
            marker=dict(
                color=products_df['total_revenue'],
                colorscale=[[0, '#0f1419'], [0.5, '#3f51b5'], [1, '#7986cb']],
                line=dict(color='#2d3748', width=1),
                colorbar=dict(
                    title="Revenue (£)",
                    tickformat="£,.0f",
                    thickness=15,
                    len=0.7
                )
            ),
            text=[f"£{x:,.0f}" for x in products_df['total_revenue']],
            textposition='outside',
            textfont=dict(color='#90caf9', size=11),
            hovertemplate='<b>%{y}</b><br>Revenue: £%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=140, r=100, t=0, b=20),
            font=dict(size=11, family="Arial, sans-serif", color="#e8eaed"),
            xaxis_title="Revenue (£)",
            xaxis_title_font=dict(color="#90caf9", size=12),
            yaxis_title="Product Code",
            yaxis_title_font=dict(color="#90caf9", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(45, 55, 72, 0.5)',
                zeroline=False
            ),
            yaxis=dict(zeroline=False)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Products Table
    st.markdown('<div class="section-header">Top Products Detailed Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    if top_products:
        products_df = pd.DataFrame(top_products[:10])
        display_df = products_df[['stock_code', 'total_quantity', 'total_revenue']].copy()
        display_df.columns = ['Product Code', 'Qty Sold', 'Revenue (£)']
        display_df['Revenue (£)'] = display_df['Revenue (£)'].apply(lambda x: f"£{x:,.0f}")
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: REVENUE
# ============================================================================

def page_revenue():
    st.markdown('<h1 class="header-title">Revenue Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Comprehensive Revenue Insights</p>', unsafe_allow_html=True)
    
    monthly_data = fetch_monthly_revenue()
    
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    if monthly_data:
        monthly_df = pd.DataFrame(monthly_data)
        monthly_df['period'] = monthly_df['year'].astype(str) + "-" + monthly_df['month'].astype(str).str.zfill(2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_df['period'],
            y=monthly_df['revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#3f51b5', width=3),
            marker=dict(size=8, color='#3f51b5', symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(63, 81, 181, 0.15)',
            hovertemplate='<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>',
            text=[f"£{x:,.0f}" for x in monthly_df['revenue']],
            textposition='top center',
            textfont=dict(color='#90caf9'),
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=70, r=20, t=20, b=70),
            font=dict(size=12, family="Arial, sans-serif", color="#e8eaed"),
            hovermode='x unified',
            xaxis_title="Month",
            xaxis_title_font=dict(color="#90caf9"),
            yaxis_title="Revenue (£)",
            yaxis_title_font=dict(color="#90caf9"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics Table
    st.markdown('<div class="section-header">Monthly Statistics</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    if monthly_data:
        monthly_df = pd.DataFrame(monthly_data)
        monthly_df['period'] = monthly_df['year'].astype(str) + "-" + monthly_df['month'].astype(str).str.zfill(2)
        display_df = monthly_df[['period', 'revenue', 'transaction_count']].copy()
        display_df.columns = ['Month', 'Revenue (£)', 'Orders']
        display_df['Revenue (£)'] = display_df['Revenue (£)'].apply(lambda x: f"£{x:,.0f}")
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Country Revenue
    st.markdown('<div class="section-header">Revenue by Country</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    country_data = fetch_country_revenue()
    if country_data:
        country_df = pd.DataFrame(country_data)
        
        fig = go.Figure(data=[go.Bar(
            x=country_df['total_revenue'],
            y=country_df['country'],
            orientation='h',
            marker=dict(
                color=country_df['total_revenue'],
                colorscale=[[0, '#0f1419'], [1, '#3f51b5']],
                line=dict(color='#2d3748', width=1)
            ),
            text=[f"£{x:,.0f}" for x in country_df['total_revenue']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Revenue: £%{x:,.0f}<extra></extra>',
            textfont=dict(color='#90caf9')
        )])
        
        fig.update_layout(
            height=500,
            margin=dict(l=180, r=80, t=0, b=20),
            font=dict(size=11, family="Arial, sans-serif", color="#e8eaed"),
            xaxis_title="Revenue (£)",
            xaxis_title_font=dict(color="#90caf9"),
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: PRODUCTS
# ============================================================================

def page_products():
    st.markdown('<h1 class="header-title">Product Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Product Performance Metrics</p>', unsafe_allow_html=True)
    
    top_products = fetch_top_products()
    
    st.markdown('<div class="section-header">Product Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">All Products Revenue Comparison</div>', unsafe_allow_html=True)
        
        if top_products:
            products_df = pd.DataFrame(top_products)
            products_df = products_df.sort_values('total_revenue', ascending=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=products_df['stock_code'],
                x=products_df['total_revenue'],
                orientation='h',
                marker=dict(
                    color=products_df['total_revenue'],
                    colorscale=[[0, '#0f1419'], [0.5, '#3f51b5'], [1, '#7986cb']],
                    line=dict(color='#2d3748', width=1),
                    colorbar=dict(
                        title="Revenue (£)",
                        tickformat="£,.0f",
                        thickness=15,
                        len=0.9
                    )
                ),
                text=[f"£{x:,.0f}" for x in products_df['total_revenue']],
                textposition='outside',
                textfont=dict(color='#90caf9', size=9),
                hovertemplate='<b>%{y}</b><br>Revenue: £%{x:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=700,
                margin=dict(l=140, r=100, t=0, b=20),
                font=dict(size=10, family="Arial, sans-serif", color="#e8eaed"),
                xaxis_title="Total Revenue (£)",
                xaxis_title_font=dict(color="#90caf9", size=11),
                yaxis_title="Product Code",
                yaxis_title_font=dict(color="#90caf9", size=11),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(45, 55, 72, 0.5)',
                    zeroline=False
                ),
                yaxis=dict(zeroline=False)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Quantity Sold vs Revenue Analysis</div>', unsafe_allow_html=True)
        
        if top_products:
            products_df = pd.DataFrame(top_products)
            
            # Calculate ranks
            products_df = products_df.sort_values('total_revenue', ascending=False).reset_index(drop=True)
            products_df['rank'] = range(1, len(products_df) + 1)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=products_df['total_quantity'],
                y=products_df['total_revenue'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=products_df['rank'],
                    colorscale=[[0, '#4caf50'], [1, '#e53935']],
                    line=dict(color='#2d3748', width=1),
                    showscale=True,
                    colorbar=dict(
                        title="Rank",
                        thickness=15,
                        len=0.9
                    )
                ),
                text=products_df['stock_code'],
                textposition='top center',
                textfont=dict(color='#90caf9', size=9),
                hovertemplate='<b>%{text}</b><br>Qty Sold: %{x:,}<br>Revenue: £%{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=700,
                margin=dict(l=80, r=100, t=20, b=60),
                font=dict(size=11, family="Arial, sans-serif", color="#e8eaed"),
                xaxis_title="Quantity Sold (Units)",
                xaxis_title_font=dict(color="#90caf9", size=11),
                yaxis_title="Total Revenue (£)",
                yaxis_title_font=dict(color="#90caf9", size=11),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Products Table
    st.markdown('<div class="section-header">Complete Product Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    if top_products:
        products_df = pd.DataFrame(top_products)
        display_df = products_df[['stock_code', 'total_quantity', 'total_revenue']].copy()
        display_df.columns = ['Product Code', 'Qty Sold', 'Revenue (£)']
        display_df['Revenue (£)'] = display_df['Revenue (£)'].apply(lambda x: f"£{x:,.0f}")
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: CUSTOMERS
# ============================================================================

def page_customers():
    st.markdown('<h1 class="header-title">Customer Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Customer Insights & Demographics</p>', unsafe_allow_html=True)
    
    top_customers = fetch_top_customers()
    
    st.markdown('<div class="section-header">Top Customers</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    if top_customers:
        customers_df = pd.DataFrame(top_customers)
        
        fig = go.Figure(data=[go.Bar(
            y=customers_df['customer_id'],
            x=customers_df['total_spent'],
            orientation='h',
            marker=dict(
                color=customers_df['transaction_count'],
                colorscale=[[0, '#0f1419'], [1, '#3f51b5']],
                line=dict(color='#2d3748', width=1)
            ),
            text=[f"£{x:,.0f}" for x in customers_df['total_spent']],
            textposition='outside',
            hovertemplate='<b>Customer %{y}</b><br>Spent: £%{x:,.0f}<extra></extra>',
            textfont=dict(color='#90caf9')
        )])
        
        fig.update_layout(
            height=450,
            margin=dict(l=100, r=80, t=0, b=20),
            font=dict(size=11, family="Arial, sans-serif", color="#e8eaed"),
            xaxis_title="Total Spent (£)",
            xaxis_title_font=dict(color="#90caf9"),
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer Rankings
    st.markdown('<div class="section-header">Customer Rankings</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    if top_customers:
        customers_df = pd.DataFrame(top_customers)
        display_df = customers_df[['customer_id', 'total_spent', 'transaction_count']].copy()
        display_df.columns = ['Customer ID', 'Total Spent (£)', 'Orders']
        display_df['Total Spent (£)'] = display_df['Total Spent (£)'].apply(lambda x: f"£{x:,.0f}")
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter by Country
    st.markdown('<div class="section-header">Filter by Country</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1], gap="small")
    
    with col1:
        country = st.selectbox(
            "Select Country",
            ["UNITED KINGDOM", "EIRE", "GERMANY", "FRANCE", "NETHERLANDS", "BELGIUM", "SWEDEN", "ITALY", "SPAIN"],
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("Search", use_container_width=True)
    
    if search_btn:
        customer_data = fetch_customer_by_country(country)
        if customer_data and customer_data.get('data'):
            customers = customer_data['data']
            st.markdown(f'<div class="success-box">Found {len(customers)} customers in {country}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
            customers_df = pd.DataFrame(customers)
            st.dataframe(customers_df[['customer_id', 'country']], use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">No customers found in {country}</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: SEARCH
# ============================================================================

def page_search():
    st.markdown('<h1 class="header-title">Product Search</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Find Products in Catalog</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Search Products</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1], gap="small")
    
    with col1:
        search_query = st.text_input(
            "Enter product name or keyword",
            placeholder="e.g., CHRISTMAS, LIGHT, CERAMIC, MUG",
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("Search", use_container_width=True, key="search_button")
    
    if search_btn and search_query:
        results = search_products(search_query)
        
        if results:
            st.markdown(f'<div class="success-box">Found {len(results)} products matching "{search_query}"</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
            results_df = pd.DataFrame(results)
            
            display_cols = ['stock_code', 'description', 'current_price']
            display_df = results_df[display_cols].copy()
            display_df.columns = ['Product Code', 'Description', 'Price']
            display_df['Price'] = display_df['Price'].apply(lambda x: f"£{x:.2f}" if x else "N/A")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">No products found for "{search_query}"</div>', unsafe_allow_html=True)
    
    elif search_btn:
        st.markdown('<div class="warning-box">Please enter a search term</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN LOGIC
# ============================================================================

if page == "Overview":
    page_overview()
elif page == "Revenue":
    page_revenue()
elif page == "Products":
    page_products()
elif page == "Customers":
    page_customers()
elif page == "Search":
    page_search()