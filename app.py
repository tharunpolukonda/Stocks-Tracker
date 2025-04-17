import streamlit as st
import yfinance as yf
import pandas as pd
import json
import datetime
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
import uuid
import time
from github import Github
import base64

# Set page title and configuration
st.set_page_config(page_title="Sector-based Stock Tracker", layout="wide")

# Access GitHub credentials from secrets
GITHUB_TOKEN = st.secrets["github"]["token"]
REPO_NAME = st.secrets["github"]["repo"]
BRANCH = st.secrets["github"]["branch"]
FILE_PATH = st.secrets["github"]["file_path"]

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Custom CSS for 3D UI with black background and blue-white accents
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #3B82F6;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #3B82F6, #1E40AF);
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4), -3px -3px 6px rgba(255, 255, 255, 0.1);
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(145deg, #2563EB, #1E3A8A);
        transform: translateY(-2px);
    }
    .stButton>button:focus {
        background: linear-gradient(145deg, #1E40AF, #1E3A8A);
        box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Primary button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(145deg, #1E40AF, #1E3A8A);
        color: #FFFFFF;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(145deg, #2563EB, #1E40AF);
        transform: translateY(-2px);
    }
    
    /* Form labels */
    .stForm label, .stTextInput label, .stNumberInput label, 
    .stDateInput label, .stSelectbox label {
        color: #3B82F6 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Text inputs and select boxes */
    .stTextInput>div>input,
    .stNumberInput>div>input,
    .stDateInput>div>input,
    .stSelectbox>div>div>select {
        background: linear-gradient(145deg, #FFFFFF, #F5F8FF);
        color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-radius: 8px;
        padding: 8px;
        box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        width: 100%;
        background: #FFFFFF;
        border-radius: 10px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5), -5px -5px 10px rgba(255, 255, 255, 0.1);
    }
    .stDataFrame table {
        background: #FFFFFF;
        color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
    }
    .stDataFrame th {
        background: linear-gradient(145deg, #3B82F6, #1E40AF);
        color: #FFFFFF;
        border: 2px solid #3B82F6;
        padding: 10px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    .stDataFrame td {
        background: #FFFFFF;
        color: #1E3A8A;
        border: 2px solid #3B82F6;
        padding: 10px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(145deg, #1E3A8A, #000000);
        color: #FFFFFF;
        border-right: 2px solid #3B82F6;
        box-shadow: 5px 0 10px rgba(0, 0, 0, 0.5);
    }
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stInfo,
    .css-1d391kg .stError,
    .css-1d391kg .stSuccess {
        color: #FFFFFF;
    }
    
    /* Info, Warning, Error, Success messages */
    .stInfo, .stWarning, .stError, .stSuccess {
        background: linear-gradient(145deg, #FFFFFF, #F5F8FF);
        color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-radius: 8px;
        box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(145deg, #FFFFFF, #F5F8FF);
        border: 2px solid #3B82F6;
        border-radius: 10px;
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.1);
        padding: 10px;
    }
    .stMetric label {
        color: #3B82F6 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    .stMetric div[data-testid="stMetricValue"] {
        color: #3B82F6 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    .stMetric div[data-testid="stMetricDelta"] {
        color: #3B82F6 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Expander */
    .streamlit-expander {
        background: linear-gradient(145deg, #FFFFFF, #F5F8FF);
        color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-radius: 10px;
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    }
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #3B82F6, #1E40AF);
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Horizontal line */
    hr {
        border-color: #3B82F6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Plotly charts */
    .js-plotly-plot .plotly .modebar {
        background-color: #1E3A8A;
        border-radius: 5px;
    }
            
    .sector-metrics-container {
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background: linear-gradient(145deg, #1E3A8A, #000000);
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    }
    .table-container {
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        background: linear-gradient(145deg, #FFFFFF, #F5F8FF);
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    }
    .table-row {
        border-bottom: 1px solid #3B82F6;
        padding: 10px 0;
        display: flex;
        align-items: center;
    }
    .table-cell {
        border-right: 1px solid #3B82F6;
        padding: 5px 10px;
        color: #1E3A8A;
    }
    .table-cell:last-child {
        border-right: none;
    }
    .company-details-container {
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        background: linear-gradient(145deg, #1E3A8A, #000000);
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    }
    .ipo-details-container {
        border: 2px solid #00FF00;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        background: linear-gradient(145deg, #1E3A8A, #000000);
        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
    }
    span[style*='color: #00FF00'] {
        font-weight: bold;
    }        
    </style>
""", unsafe_allow_html=True)

# Define functions for data management
def save_data(data):
    """Save data to stock_data.json on GitHub"""
    try:
        # Get the current file's SHA (required for updates)
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        repo.update_file(
            path=FILE_PATH,
            message="Update stock_data.json with new data",
            content=json.dumps(data, indent=4).encode('utf-8'),
            sha=contents.sha,
            branch=BRANCH
        )
        print(f"Successfully updated {FILE_PATH} in {REPO_NAME}")
    except Exception as e:
        # If file doesn't exist, create it
        if "404" in str(e):
            try:
                repo.create_file(
                    path=FILE_PATH,
                    message="Create stock_data.json",
                    content=json.dumps(data, indent=4).encode('utf-8'),
                    branch=BRANCH
                )
                print(f"Successfully created {FILE_PATH} in {REPO_NAME}")
            except Exception as create_e:
                print(f"Failed to create {FILE_PATH}: {str(create_e)}")
                raise create_e
        else:
            print(f"Failed to update {FILE_PATH}: {str(e)}")
            raise e

def load_data():
    """Load data from stock_data.json on GitHub or initialize empty structure"""
    try:
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        # Decode base64 content
        decoded_content = base64.b64decode(contents.content).decode("utf-8")
        data = json.loads(decoded_content)
        # Ensure all companies have required fields
        for company in data.get("companies", []):
            if "id" not in company:
                company["id"] = str(uuid.uuid4())
            if "total_invested" not in company:
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                company["total_invested"] = buy_price * shares
            if "profit_until_now" not in company:
                company["profit_until_now"] = 0.0
            if "loss_until_now" not in company:
                company["loss_until_now"] = 0.0
            # Initialize IPO fields if missing
            if "listing_price" not in company:
                company["listing_price"] = 0.0
            if "issue_price" not in company:
                company["issue_price"] = 0.0
            if "issue_size" not in company:
                company["issue_size"] = 0
            if "listed_date" not in company:
                company["listed_date"] = ""
            if "grow_link" not in company:
                company["grow_link"] = ""
            # Initialize transaction for existing companies with shares
            if company.get("shares", 0) > 0 and company["total_invested"] > 0:
                if not any(t["company_id"] == company["id"] for t in data.get("transactions", [])):
                    transaction = {
                        "company_id": company["id"],
                        "type": "buy",
                        "amount": company["total_invested"],
                        "shares": company["shares"],
                        "price_per_share": company["buy_price"],
                        "date": company.get("purchase_date", datetime.date.today().strftime("%Y-%m-%d")),
                        "profit_loss": 0.0
                    }
                    data["transactions"] = data.get("transactions", []) + [transaction]
        save_data(data)  # Save updated data
        return data
    except Exception as e:
        print(f"Failed to load {FILE_PATH}: {str(e)}")
        # If file doesn't exist or can't be accessed, return empty structure
        data = {
            "sectors": [],
            "companies": [],
            "transactions": []
        }
        save_data(data)  # Create the file on GitHub
        return data

def get_current_stock_price(symbol):
    """Fetch current stock price using yfinance"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            current_price = data["Close"].iloc[-1]
            return round(current_price, 2)
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

def get_today_return(ticker_symbol):
    if 'return_cache' not in st.session_state:
        st.session_state.return_cache = {}
    
    today = datetime.date.today()
    cache_key = f"{ticker_symbol}_{today.strftime('%Y-%m-%d')}"
    if cache_key in st.session_state.return_cache:
        return st.session_state.return_cache[cache_key]
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker_symbol)
            # Fetch 7 days to ensure enough data
            data = stock.history(start=today - timedelta(days=7), end=today + timedelta(days=1), interval="1d")
            
            if len(data) < 2:
                print(f"Error for {ticker_symbol}: Not enough data, only {len(data)} days")
                return None, f"Not enough data: {len(data)} days"
            
            # Get the two most recent trading days
            sorted_dates = sorted(data.index, reverse=True)
            today_str = today.strftime('%Y-%m-%d')
            
            # Try today's close, else use the latest available
            today_close = None
            latest_date = sorted_dates[0].strftime('%Y-%m-%d')
            if latest_date <= today_str:
                today_close = data.loc[latest_date]["Close"]
            
            # Get previous trading day's close
            previous_close = None
            previous_date = None
            if len(sorted_dates) > 1:
                previous_date = sorted_dates[1].strftime('%Y-%m-%d')
                previous_close = data.loc[previous_date]["Close"]
            
            if today_close is None or previous_close is None:
                print(f"Error for {ticker_symbol}: Missing price data - today_close={today_close}, previous_close={previous_close}")
                return None, "Missing price data"
            
            if previous_close == 0:
                print(f"Error for {ticker_symbol}: Zero close price on {previous_date}")
                return None, "Invalid data: Zero close price"
            
            return_pct = ((today_close - previous_close) / previous_close) * 100
            return_value = round(return_pct, 2)
            
            st.session_state.return_cache[cache_key] = (return_value, f"{previous_date} to {latest_date}")
            print(f"Success for {ticker_symbol}: {return_value}% from {previous_date} to {latest_date}")
            return return_value, f"{previous_date} to {latest_date}"
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {ticker_symbol}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None, f"Error: {str(e)}"

def calculate_profit_loss(buy_price, shares, current_price):
    """Calculate profit/loss for a position"""
    if buy_price is not None and shares is not None and current_price is not None:
        invested_amount = float(buy_price) * float(shares)
        current_value = float(current_price) * float(shares)
        profit_loss = current_value - invested_amount
        profit_loss_percent = (profit_loss / invested_amount) * 100 if invested_amount > 0 else 0
        return {
            "invested_amount": round(invested_amount, 2),
            "current_value": round(current_value, 2),
            "profit_loss": round(profit_loss, 2),
            "profit_loss_percent": round(profit_loss_percent, 2)
        }
    return None

def get_indian_market_cap_category(ticker_symbol):
    """Classify company based on market cap"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        market_cap_crore = ticker.info.get('marketCap') / 10_000_000
        
        if market_cap_crore is None:
            return None, f"Could not retrieve market cap for {ticker_symbol}"
        
        if market_cap_crore >= 20000:
            category = "Large-Cap"
        elif 5000 <= market_cap_crore < 20000:
            category = "Mid-Cap"
        elif 1000 <= market_cap_crore < 5000:
            category = "Small-Cap"
        else:
            category = "Micro-Cap"
        
        return category, round(market_cap_crore, 2)
    except Exception as e:
        return None, f"Error processing {ticker_symbol}: {str(e)}"

# Initialize session state for managing app state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
    
if 'add_sector_clicked' not in st.session_state:
    st.session_state.add_sector_clicked = False
    
if 'add_company_clicked' not in st.session_state:
    st.session_state.add_company_clicked = False
    
if 'add_ipo_clicked' not in st.session_state:
    st.session_state.add_ipo_clicked = False
    
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = False
    
if 'selected_sector_for_view' not in st.session_state:
    st.session_state.selected_sector_for_view = None

if 'show_high_return' not in st.session_state:
    st.session_state.show_high_return = False

if 'high_return_sector' not in st.session_state:
    st.session_state.high_return_sector = "All Sectors"

if 'show_hx_cat' not in st.session_state:
    st.session_state.show_hx_cat = False

if 'show_invest_companies' not in st.session_state:
    st.session_state.show_invest_companies = False

if 'invest_companies_sector' not in st.session_state:
    st.session_state.invest_companies_sector = "All Sectors"

if 'show_visualize_companies' not in st.session_state:
    st.session_state.show_visualize_companies = False

if 'visualize_sector' not in st.session_state:
    st.session_state.visualize_sector = "All Sectors"

if 'filter_cap_wise' not in st.session_state:
    st.session_state.filter_cap_wise = False

if 'selected_cap' not in st.session_state:
    st.session_state.selected_cap = "Large-Cap"

if 'filter_combined_caps' not in st.session_state:
    st.session_state.filter_combined_caps = False

if 'show_journal_ledger' not in st.session_state:
    st.session_state.show_journal_ledger = False

if 'edit_company' not in st.session_state:
    st.session_state.edit_company = None

if 'view_company_details' not in st.session_state:
    st.session_state.view_company_details = None

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_add_ipo():
    st.session_state.add_ipo_clicked = not st.session_state.add_ipo_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_view_mode():
    st.session_state.view_mode = not st.session_state.view_mode
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.view_mode:
        st.session_state.selected_sector_for_view = None

def toggle_high_return():
    st.session_state.show_high_return = not st.session_state.show_high_return
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_high_return:
        st.session_state.high_return_sector = "All Sectors"

def toggle_hx_cat():
    st.session_state.show_hx_cat = not st.session_state.show_hx_cat
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_invest_companies():
    st.session_state.show_invest_companies = not st.session_state.show_invest_companies
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_invest_companies:
        st.session_state.invest_companies_sector = "All Sectors"

def toggle_visualize_companies():
    st.session_state.show_visualize_companies = not st.session_state.show_visualize_companies
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_visualize_companies:
        st.session_state.visualize_sector = "All Sectors"

def toggle_journal_ledger():
    st.session_state.show_journal_ledger = not st.session_state.show_journal_ledger
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_filter_cap_wise():
    st.session_state.filter_cap_wise = not st.session_state.filter_cap_wise
    st.session_state.filter_combined_caps = False
    if st.session_state.filter_cap_wise:
        st.session_state.selected_cap = "Large-Cap"

def toggle_filter_combined_caps():
    st.session_state.filter_combined_caps = not st.session_state.filter_combined_caps
    st.session_state.filter_cap_wise = False

def set_selected_sector(sector):
    st.session_state.selected_sector_for_view = sector

def toggle_edit_company(company_id):
    st.session_state.edit_company = company_id if st.session_state.edit_company != company_id else None

def go_to_home():
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.selected_sector_for_view = None
    st.session_state.edit_company = None
    st.rerun()

# App title and description
st.title("📈 HOOX Companywise Tracker & Analysis")
st.markdown("Track stock prices organized by business sectors")

# Action buttons at the top
st.markdown("### Actions")
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
with col1:
    if st.button("Home", key="home_button"):
        go_to_home()
with col2:
    if st.button("Add Sector", key="add_sector_button"):
        toggle_add_sector()
with col3:
    if st.button("Add Company", key="add_company_button"):
        toggle_add_company()
with col4:
    if st.button("Add IPOs", key="add_ipo_button"):
        toggle_add_ipo()
with col5:
    if st.button("View Sectors", key="view_mode_button", 
                 type="primary" if st.session_state.view_mode else "secondary"):
        toggle_view_mode()
with col6:
    if st.button("High Return", key="high_return_button",
                 type="primary" if st.session_state.show_high_return else "secondary"):
        toggle_high_return()
with col7:
    if st.button("Track-HX-CAT", key="hx_cat_button",
                 type="primary" if st.session_state.show_hx_cat else "secondary"):
        toggle_hx_cat()
with col8:
    if st.button("Track_Invest", key="invest_companies_button",
                 type="primary" if st.session_state.show_invest_companies else "secondary"):
        toggle_invest_companies()
with col9:
    if st.button("Visualize Companies", key="visualize_companies_button",
                 type="primary" if st.session_state.show_visualize_companies else "secondary"):
        toggle_visualize_companies()
with col10:
    if st.button("Journal & Ledger", key="journal_ledger_button",
                 type="primary" if st.session_state.show_journal_ledger else "secondary"):
        toggle_journal_ledger()

st.markdown("---")

# Add Sector Form
if st.session_state.add_sector_clicked:
    st.subheader("Add New Sector")
    with st.form("add_sector_form"):
        sector_name = st.text_input("Sector Name", placeholder="e.g. Technology")
        submit_sector = st.form_submit_button("Add Sector")
        
        if submit_sector and sector_name:
            if sector_name not in st.session_state.data["sectors"]:
                st.session_state.data["sectors"].append(sector_name)
                save_data(st.session_state.data)
                st.success(f"Sector '{sector_name}' added successfully!")
                st.session_state.add_sector_clicked = False
                st.rerun()
            else:
                st.error(f"Sector '{sector_name}' already exists!")

# Add Company Form
if st.session_state.add_company_clicked:
    st.subheader("Add Company to Track")
    
    if not st.session_state.data["sectors"]:
        st.warning("Please add at least one sector first!")
    else:
        with st.form("add_company_form"):
            company_name = st.text_input("Company Name", placeholder="e.g. Reliance Industries")
            ticker_code = st.text_input("Ticker Code", placeholder="e.g. RELIANCE")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"])
            
            buy_price = st.number_input("Buy Price", min_value=0.00, value=0.00, format="%.2f", 
                                       placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=0, value=0, step=1, 
                                    placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", 
                                         value=datetime.date.today(),
                                         max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO"]
            suffix = st.selectbox("Exchange Suffix", suffix_options, 
                                  index=0, 
                                  help=".NS for NSE, .BO for BSE")
            
            move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], 
                                     help="Select Yes to tag as HX-CAT")
            
            submit_company = st.form_submit_button("Add Company")
            
            if submit_company and company_name and ticker_code:
                full_ticker = f"{ticker_code}{suffix}"
                
                existing_tickers = [company["ticker"] for company in st.session_state.data["companies"]]
                if full_ticker in existing_tickers:
                    st.error(f"Company with ticker '{full_ticker}' already exists!")
                else:
                    test_price = get_current_stock_price(full_ticker)
                    if test_price is not None:
                        new_company = {
                            "id": str(uuid.uuid4()),
                            "name": company_name,
                            "ticker": full_ticker,
                            "sector": selected_sector,
                            "buy_price": float(buy_price),
                            "shares": int(shares),
                            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                            "hx_cat": move_to_hx == "Yes",
                            "total_invested": float(buy_price) * int(shares),
                            "profit_until_now": 0.0,
                            "loss_until_now": 0.0,
                            "listing_price": 0.0,
                            "issue_price": 0.0,
                            "issue_size": 0,
                            "listed_date": "",
                            "grow_link": ""
                        }
                        st.session_state.data["companies"].append(new_company)
                        # Log transaction if shares > 0
                        if shares > 0 and buy_price > 0:
                            transaction = {
                                "company_id": new_company["id"],
                                "type": "buy",
                                "amount": new_company["total_invested"],
                                "shares": new_company["shares"],
                                "price_per_share": new_company["buy_price"],
                                "date": new_company["purchase_date"],
                                "profit_loss": 0.0
                            }
                            st.session_state.data["transactions"].append(transaction)
                        save_data(st.session_state.data)
                        st.success(f"Company '{company_name}' added successfully!")
                        st.session_state.add_company_clicked = False
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
            elif submit_company:
                st.error("Please fill Company Name and Ticker Code.")

# Add IPOs Form
if st.session_state.add_ipo_clicked:
    st.subheader("Add IPO to Track")
    
    if not st.session_state.data["sectors"]:
        st.warning("Please add at least one sector first!")
    else:
        with st.form("add_ipo_form"):
            company_name = st.text_input("Company Name", placeholder="e.g. Ola Electric")
            ticker_code = st.text_input("Ticker Code", placeholder="e.g. OLA")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"])
            
            buy_price = st.number_input("Buy Price", min_value=0.00, value=0.00, format="%.2f", 
                                       placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=0, value=0, step=1, 
                                    placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", 
                                         value=datetime.date.today(),
                                         max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO"]
            suffix = st.selectbox("Exchange Suffix", suffix_options, 
                                  index=0, 
                                  help=".NS for NSE, .BO for BSE")
            
            move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], 
                                     help="Select Yes to tag as HX-CAT")
            
            listing_price = st.number_input("Listing Price", min_value=0.00, value=0.00, format="%.2f", 
                                           placeholder="Enter listing price")
            issue_price = st.number_input("Issue Price", min_value=0.00, value=0.00, format="%.2f", 
                                         placeholder="Enter issue price")
            issue_size = st.number_input("Issue Size (in shares)", min_value=0, value=0, step=1, 
                                        placeholder="Enter issue size")
            listed_date = st.date_input("Listed Date", 
                                       value=datetime.date.today(),
                                       max_value=datetime.date.today())
            grow_link = st.text_input("GrowLink", placeholder="e.g. https://groww.in/ipo/ola-electric")
            
            submit_ipo = st.form_submit_button("Add IPO")
            
            if submit_ipo and company_name and ticker_code:
                full_ticker = f"{ticker_code}{suffix}"
                
                existing_tickers = [company["ticker"] for company in st.session_state.data["companies"]]
                if full_ticker in existing_tickers:
                    st.error(f"Company with ticker '{full_ticker}' already exists!")
                else:
                    test_price = get_current_stock_price(full_ticker)
                    if test_price is not None:
                        new_company = {
                            "id": str(uuid.uuid4()),
                            "name": company_name,
                            "ticker": full_ticker,
                            "sector": selected_sector,
                            "buy_price": float(buy_price),
                            "shares": int(shares),
                            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                            "hx_cat": move_to_hx == "Yes",
                            "total_invested": float(buy_price) * int(shares),
                            "profit_until_now": 0.0,
                            "loss_until_now": 0.0,
                            "listing_price": float(listing_price),
                            "issue_price": float(issue_price),
                            "issue_size": int(issue_size),
                            "listed_date": listed_date.strftime("%Y-%m-%d"),
                            "grow_link": grow_link
                        }
                        st.session_state.data["companies"].append(new_company)
                        # Log transaction if shares > 0
                        if shares > 0 and buy_price > 0:
                            transaction = {
                                "company_id": new_company["id"],
                                "type": "buy",
                                "amount": new_company["total_invested"],
                                "shares": new_company["shares"],
                                "price_per_share": new_company["buy_price"],
                                "date": new_company["purchase_date"],
                                "profit_loss": 0.0
                            }
                            st.session_state.data["transactions"].append(transaction)
                        save_data(st.session_state.data)
                        st.success(f"IPO '{company_name}' added successfully!")
                        st.session_state.add_ipo_clicked = False
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
            elif submit_ipo:
                st.error("Please fill Company Name and Ticker Code.")

# Edit Company Form
if st.session_state.edit_company:
    company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.edit_company), None)
    if company:
        st.subheader(f"Edit Company: {company['name']}")
        with st.form(f"edit_company_form_{company['id']}"):
            company_name = st.text_input("Company Name", value=company["name"], placeholder="e.g. Reliance Industries")
            ticker_code = st.text_input("Ticker Code", value=company["ticker"].replace(".NS", "").replace(".BO", ""), placeholder="e.g. RELIANCE")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"], index=st.session_state.data["sectors"].index(company["sector"]))
            
            buy_price = st.number_input("Buy Price", min_value=0.00, format="%.2f", value=float(company["buy_price"]), placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=0, step=1, value=int(company["shares"]), placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", value=datetime.datetime.strptime(company["purchase_date"], "%Y-%m-%d").date(), max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO"]
            current_suffix = ".NS" if company["ticker"].endswith(".NS") else ".BO" if company["ticker"].endswith(".BO") else ".NS"
            suffix = st.selectbox("Exchange Suffix", suffix_options, index=suffix_options.index(current_suffix), help=".NS for NSE, .BO for BSE")
            
            move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], index=1 if company["hx_cat"] else 0, help="Select Yes to tag as HX-CAT")
            
            # IPO fields
            listing_price = st.number_input("Listing Price", min_value=0.00, format="%.2f", value=float(company.get("listing_price", 0.0)), placeholder="Enter listing price")
            issue_price = st.number_input("Issue Price", min_value=0.00, format="%.2f", value=float(company.get("issue_price", 0.0)), placeholder="Enter issue price")
            issue_size = st.number_input("Issue Size (in shares)", min_value=0, step=1, value=int(company.get("issue_size", 0)), placeholder="Enter issue size")
            listed_date = st.date_input("Listed Date", value=datetime.datetime.strptime(company.get("listed_date", datetime.date.today().strftime("%Y-%m-%d")), "%Y-%m-%d").date() if company.get("listed_date") else datetime.date.today(), max_value=datetime.date.today())
            grow_link = st.text_input("GrowLink", value=company.get("grow_link", ""), placeholder="e.g. https://groww.in/ipo/ola-electric")
            
            col1, col2 = st.form_submit_button("Update Company"), st.form_submit_button("Cancel")
            
            if col1 and company_name and ticker_code:
                full_ticker = f"{ticker_code}{suffix}"
                
                existing_tickers = [c["ticker"] for c in st.session_state.data["companies"] if c["id"] != company["id"]]
                if full_ticker in existing_tickers:
                    st.error(f"Company with ticker '{full_ticker}' already exists!")
                else:
                    test_price = get_current_stock_price(full_ticker)
                    if test_price is not None:
                        company.update({
                            "name": company_name,
                            "ticker": full_ticker,
                            "sector": selected_sector,
                            "buy_price": float(buy_price),
                            "shares": int(shares),
                            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                            "hx_cat": move_to_hx == "Yes",
                            "total_invested": float(buy_price) * int(shares),
                            "listing_price": float(listing_price),
                            "issue_price": float(issue_price),
                            "issue_size": int(issue_size),
                            "listed_date": listed_date.strftime("%Y-%m-%d"),
                            "grow_link": grow_link
                        })
                        # Update transaction if exists, or create new one
                        existing_transaction = next((t for t in st.session_state.data["transactions"] if t["company_id"] == company["id"] and t["type"] == "buy"), None)
                        if existing_transaction and shares > 0 and buy_price > 0:
                            existing_transaction.update({
                                "amount": company["total_invested"],
                                "shares": company["shares"],
                                "price_per_share": company["buy_price"],
                                "date": company["purchase_date"],
                                "profit_loss": 0.0
                            })
                        elif shares > 0 and buy_price > 0:
                            transaction = {
                                "company_id": company["id"],
                                "type": "buy",
                                "amount": company["total_invested"],
                                "shares": company["shares"],
                                "price_per_share": company["buy_price"],
                                "date": company["purchase_date"],
                                "profit_loss": 0.0
                            }
                            st.session_state.data["transactions"].append(transaction)
                        save_data(st.session_state.data)
                        st.success(f"Company '{company_name}' updated successfully!")
                        st.session_state.edit_company = None
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
            elif col1:
                st.error("Please fill Company Name and Ticker Code.")
            elif col2:
                st.session_state.edit_company = None
                st.rerun()

# Journal & Ledger Section
if st.session_state.show_journal_ledger:
    st.header("Journal & Ledger - Transaction History")
    
    # Initialize filter options
    filter_options = ["All", "Profit Until Now", "Loss Until Now"]
    selected_filter = st.selectbox("Filter Transactions", filter_options)
    
    # Prepare data for the table
    table_data = []
    for company in st.session_state.data["companies"]:
        current_price = get_current_stock_price(company["ticker"])
        day_return, _ = get_today_return(company["ticker"])
        buy_price = company.get("buy_price", 0)
        shares = company.get("shares", 0)
        total_invested = company.get("total_invested", buy_price * shares)
        purchase_date = company.get("purchase_date", "N/A")
        profit_until_now = company.get("profit_until_now", 0.0)
        loss_until_now = company.get("loss_until_now", 0.0)
        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
        
        pl_data = None
        if current_price and shares > 0:
            pl_data = calculate_profit_loss(buy_price, shares, current_price)
        
        company_data = {
            "Company": company["name"],
            "Ticker": company["ticker"],
            "Sector": company["sector"],
            "Shares": shares,
            "Buy Price": f"{currency_symbol}{buy_price:.2f}",
            "Current Price": f"{currency_symbol}{current_price:.2f}" if current_price else "N/A",
            "Day Change": f"{day_return}%" if day_return is not None else "N/A",
            "Invested": f"{currency_symbol}{total_invested:.2f}",
            "Profit Until Now": f"{currency_symbol}{profit_until_now:.2f}",
            "Loss Until Now": f"{currency_symbol}{loss_until_now:.2f}",
            "Purchase Date": purchase_date,
            "ID": company["id"]
        }
        
        if pl_data:
            company_data.update({
                "Current Value": f"{currency_symbol}{pl_data['current_value']:.2f}",
                "P/L": f"{currency_symbol}{pl_data['profit_loss']:.2f}",
                "P/L %": f"{pl_data['profit_loss_percent']:.2f}%"
            })
        else:
            company_data.update({
                "Current Value": "N/A",
                "P/L": "N/A",
                "P/L %": "N/A"
            })
        
        # Apply filter
        if selected_filter == "All":
            table_data.append(company_data)
        elif selected_filter == "Profit Until Now" and profit_until_now > 0:
            table_data.append(company_data)
        elif selected_filter == "Loss Until Now" and loss_until_now > 0:
            table_data.append(company_data)
    
    # Display the table
    if not table_data:
        st.info("No transactions match the selected filter.")
    else:
        df = pd.DataFrame(table_data)
        st.dataframe(
            df.drop(columns=["ID"]),
            use_container_width=True,
            column_config={
                "Company": st.column_config.TextColumn(width="medium"),
                "Ticker": st.column_config.TextColumn(width="small"),
                "Sector": st.column_config.TextColumn(width="small"),
                "Shares": st.column_config.NumberColumn(width="small"),
                "Buy Price": st.column_config.TextColumn(width="small"),
                "Current Price": st.column_config.TextColumn(width="small"),
                "Day Change": st.column_config.TextColumn(width="small"),
                "Invested": st.column_config.TextColumn(width="small"),
                "Profit Until Now": st.column_config.TextColumn(width="small"),
                "Loss Until Now": st.column_config.TextColumn(width="small"),
                "Purchase Date": st.column_config.TextColumn(width="small"),
                "Current Value": st.column_config.TextColumn(width="small"),
                "P/L": st.column_config.TextColumn(width="small"),
                "P/L %": st.column_config.TextColumn(width="small")
            }
        )
    
    # Manage Transactions
    st.subheader("Manage Transactions")
    with st.form(key="transaction_form"):
        # Dropdown includes all companies, not just those with shares > 0
        company_options = {c["name"]: c["id"] for c in st.session_state.data["companies"]}
        selected_company_name = st.selectbox("Select Company", options=[""] + list(company_options.keys()))
        transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
        shares = st.number_input("Number of Shares", min_value=0, step=1)
        price_per_share = st.number_input("Price per Share (₹)", min_value=0.0, step=0.01)
        transaction_date = st.date_input("Transaction Date", value=datetime.date.today())
        submit_button = st.form_submit_button("Add Transaction")
        
        if submit_button and selected_company_name:
            company_id = company_options[selected_company_name]
            company = next(c for c in st.session_state.data["companies"] if c["id"] == company_id)
            amount = shares * price_per_share
            
            # Create transaction
            transaction = {
                "company_id": company_id,
                "type": transaction_type.lower(),
                "amount": amount,
                "shares": shares,
                "price_per_share": price_per_share,
                "date": transaction_date.strftime("%Y-%m-%d"),
                "profit_loss": 0.0
            }
            
            # Update company data
            if transaction_type == "Buy":
                company["shares"] = company.get("shares", 0) + shares
                company["total_invested"] = company.get("total_invested", 0) + amount
                company["buy_price"] = price_per_share if company["shares"] == shares else (
                    (company.get("buy_price", 0) * company.get("shares", 0) + amount) / company["shares"]
                )
                company["purchase_date"] = transaction_date.strftime("%Y-%m-%d")
            elif transaction_type == "Sell":
                if shares > company.get("shares", 0):
                    st.error("Cannot sell more shares than owned!")
                else:
                    company["shares"] = company.get("shares", 0) - shares
                    company["total_invested"] = company.get("total_invested", 0) - (shares * company.get("buy_price", 0))
                    profit_loss = (price_per_share - company.get("buy_price", 0)) * shares
                    transaction["profit_loss"] = profit_loss
                    if profit_loss > 0:
                        company["profit_until_now"] = company.get("profit_until_now", 0) + profit_loss
                    else:
                        company["loss_until_now"] = company.get("loss_until_now", 0) + abs(profit_loss)
                    if company["shares"] == 0:
                        company["total_invested"] = 0
                        company["buy_price"] = 0
            
            # Add transaction to data
            st.session_state.data["transactions"].append(transaction)
            save_data(st.session_state.data)
            st.success(f"Transaction added for {selected_company_name}!")
            st.rerun()

# Visualize Companies Section
if st.session_state.show_visualize_companies:
    st.header("Company Investment Analysis")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        sectors = ["All Sectors"] + st.session_state.data["sectors"]
        sector_key = "visualize_sector_filter"
        
        selected_sector = st.selectbox(
            "Filter by Sector",
            sectors,
            index=sectors.index(st.session_state.visualize_sector),
            key=sector_key
        )
        
        if selected_sector != st.session_state.visualize_sector:
            st.session_state.visualize_sector = selected_sector
            st.session_state.filter_cap_wise = False
            st.session_state.filter_combined_caps = False
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("Filter Cap Wise", key="filter_cap_wise_button",
                        type="primary" if st.session_state.filter_cap_wise else "secondary"):
                toggle_filter_cap_wise()
        with col3:
            if st.button("Filter Combined Caps", key="filter_combined_caps_button",
                        type="primary" if st.session_state.filter_combined_caps else "secondary"):
                toggle_filter_combined_caps()

        # Sector-based Visualization
        if not st.session_state.filter_cap_wise and not st.session_state.filter_combined_caps:
            data = []
            total_invested = 0
            total_pl = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])
                    
                    pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None
                    
                    if total_invested_company > 0:
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        if pl_data:
                            total_pl += pl_data["profit_loss"]
                        data.append(company_data)
            
            if not data:
                st.info(f"No invested companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")
                
                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display combined P/L
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    pl_label = "Profit" if total_pl >= 0 else "Loss"
                    st.metric(f"Combined {pl_label} for {selected_sector}", 
                             f"{currency_symbol}{abs(total_pl):.2f}")

        # Cap-wise Visualization
        elif st.session_state.filter_cap_wise:
            cap_categories = ["Large-Cap", "Mid-Cap", "Small-Cap", "Micro-Cap"]
            selected_cap = st.selectbox(
                "Select Market Cap Category",
                cap_categories,
                index=cap_categories.index(st.session_state.selected_cap),
                key="cap_filter"
            )
            
            if selected_cap != st.session_state.selected_cap:
                st.session_state.selected_cap = selected_cap
            
            data = []
            total_invested = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])
                    
                    cap_category, _ = get_indian_market_cap_category(company["ticker"])
                    
                    if cap_category == selected_cap and total_invested_company > 0:
                        pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        data.append(company_data)
            
            if not data:
                st.info(f"No {selected_cap} companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")
                
                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"{selected_cap} Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)

        # Combined Caps Visualization
        elif st.session_state.filter_combined_caps:
            data = []
            total_invested = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])
                    
                    if total_invested_company > 0:
                        pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        data.append(company_data)
            
            if not data:
                st.info(f"No invested companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")
                
                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"All Companies Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)

# HX-CAT Section
if st.session_state.show_hx_cat:
    st.header("HX-CAT Companies")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        data = []
        for company in st.session_state.data["companies"]:
            if company.get("hx_cat", False):
                day_return, _ = get_today_return(company["ticker"])
                if day_return is not None:
                    data.append({
                        "Company": company["name"],
                        "Sector": company["sector"],
                        "Day Change (%)": day_return
                    })
        
        if not data:
            st.info("No companies tagged as HX-CAT found.")
        else:
            df = pd.DataFrame(data)
            df = df.sort_values(by="Day Change (%)", ascending=False)
            df = df.reset_index(drop=True)
            
            st.subheader("HX-CAT Companies Ranked by Daily Return")
            st.dataframe(df, use_container_width=True)

# Invest Companies Section
if st.session_state.show_invest_companies:
    st.header("Invested Companies")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        sectors = ["All Sectors"] + st.session_state.data["sectors"]
        sector_key = "invest_companies_sector_filter"
        
        selected_sector = st.selectbox(
            "Filter by Sector",
            sectors,
            index=sectors.index(st.session_state.invest_companies_sector),
            key=sector_key
        )
        
        if selected_sector != st.session_state.invest_companies_sector:
            st.session_state.invest_companies_sector = selected_sector
        
        data = []
        for company in st.session_state.data["companies"]:
            total_invested = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
            if company["shares"] > 0 and (selected_sector == "All Sectors" or company["sector"] == selected_sector):
                day_return, _ = get_today_return(company["ticker"])
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                
                company_data = {
                    "Company": company["name"],
                    "Sector": company["sector"],
                    "Ticker": company["ticker"],
                    "Purchase Date": company.get("purchase_date", "N/A"),
                    "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                    "Shares": shares,
                    "Invested": f"{currency_symbol}{total_invested:.2f}",
                    "Day Change (%)": day_return if day_return is not None else "N/A"
                }
                data.append(company_data)
        
        if not data:
            st.info(f"No invested companies found for {selected_sector}.")
        else:
            df = pd.DataFrame(data)
            st.subheader(f"Invested Companies")
            st.dataframe(df, use_container_width=True)

# High Return Section
if st.session_state.show_high_return:
    st.header("High Return Stocks")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        sectors = ["All Sectors"] + st.session_state.data["sectors"]
        sector_key = "high_return_sector_filter"
        
        selected_sector = st.selectbox(
            "Filter by Sector",
            sectors,
            index=sectors.index(st.session_state.high_return_sector),
            key=sector_key
        )
        
        if selected_sector != st.session_state.high_return_sector:
            st.session_state.high_return_sector = selected_sector
        
        data = []
        for company in st.session_state.data["companies"]:
            if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                day_return, _ = get_today_return(company["ticker"])
                if day_return is not None:
                    data.append({
                        "Company": company["name"],
                        "Sector": company["sector"],
                        "Day Change (%)": day_return
                    })
        
        if not data:
            st.info(f"No companies with valid data found for {selected_sector}.")
        else:
            df = pd.DataFrame(data)
            df = df.sort_values(by="Day Change (%)", ascending=False)
            df = df.reset_index(drop=True)
            
            st.subheader(f"Stocks Ranked by Daily Return")
            st.dataframe(df, use_container_width=True)

# View Mode Section
if st.session_state.view_mode:
    st.header("View Mode - Portfolio by Sector")
    
    if not st.session_state.data["sectors"]:
        st.info("No sectors added yet. Click 'Add Sector' to get started.")
    elif not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        # Check if viewing company details
        if "view_company_details" in st.session_state and st.session_state.view_company_details:
            company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.view_company_details), None)
            if company:
                st.markdown('<div class="company-details-container">', unsafe_allow_html=True)
                st.subheader(f"Details for {company['name']}")
                is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))
                current_price = get_current_stock_price(company["ticker"])
                day_return, day_return_msg = get_today_return(company["ticker"])
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                total_invested = company.get("total_invested", buy_price * shares)
                currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                ticker_suffix = "NS" if company["ticker"].endswith(".NS") else "BO" if company["ticker"].endswith(".BO") else "Other"
                
                pl_data = None
                if current_price and shares > 0:
                    pl_data = calculate_profit_loss(buy_price, shares, current_price)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Company Name**: {company['name']}")
                    st.markdown(f"**Sector**: {company['sector']}")
                    st.markdown(f"**Ticker Code**: {company['ticker']}")
                    st.markdown(f"**Ticker Suffix**: {ticker_suffix}")
                    st.markdown(f"**Number of Shares**: {shares}")
                    st.markdown(f"**Each Share Price (Buy)**: {currency_symbol}{buy_price:.2f}")
                with col2:
                    st.markdown(f"**Day Change**: {day_return}% {'(N/A: ' + day_return_msg + ')' if day_return is None else ''}")
                    st.markdown(f"**Current Value**: {currency_symbol}{pl_data['current_value']:.2f} {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**P/L**: {currency_symbol}{pl_data['profit_loss']:.2f} {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**P/L %**: {pl_data['profit_loss_percent']:.2f}% {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**Type**: {'IPO' if is_ipo else 'Regular'}")
                
                if is_ipo:
                    st.markdown('<div class="ipo-details-container">', unsafe_allow_html=True)
                    st.subheader("IPO Details")
                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown(f"**Listing Price**: {currency_symbol}{company.get('listing_price', 0):.2f}")
                        st.markdown(f"**Issue Price**: {currency_symbol}{company.get('issue_price', 0):.2f}")
                    with col4:
                        st.markdown(f"**Issue Size**: {company.get('issue_size', 0)}")
                        st.markdown(f"**Listed Date**: {company.get('listed_date', 'N/A')}")
                        if company.get("grow_link"):
                            st.markdown(f"**Grow Link**: [{company['grow_link']}]({company['grow_link']})")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("Back to Sector"):
                    st.session_state.view_company_details = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Sector selection or table view
        elif st.session_state.selected_sector_for_view is None:
            st.subheader("Select a Sector to View")
            
            cols = st.columns(3)
            
            for i, sector in enumerate(st.session_state.data["sectors"]):
                sector_companies = [c for c in st.session_state.data["companies"] if c["sector"] == sector]
                
                with cols[i % 3]:
                    st.markdown(f"### {sector}")
                    st.markdown(f"**Companies:** {len(sector_companies)}")
                    
                    if sector_companies:
                        sector_invested = sum(c.get("total_invested", c.get("buy_price", 0) * c.get("shares", 0)) for c in sector_companies)
                        st.markdown(f"**Invested:** ₹{sector_invested:.2f}")
                    
                    if st.button(f"View {sector}", key=f"view_{sector}"):
                        set_selected_sector(sector)
                        st.rerun()
        
        else:
            selected_sector = st.session_state.selected_sector_for_view
            sector_companies = [c for c in st.session_state.data["companies"] if c["sector"] == selected_sector]
            
            if st.button("← Back to Sectors"):
                st.session_state.selected_sector_for_view = None
                st.rerun()
                
            st.subheader(f"{selected_sector} Sector Analysis")
            
            if not sector_companies:
                st.info(f"No companies added to the {selected_sector} sector yet.")
            else:
                sector_invested = sum(c.get("total_invested", c.get("buy_price", 0) * c.get("shares", 0)) for c in sector_companies)
                sector_current_value = 0
                sector_pl = 0
                
                # Sector metrics
                st.markdown('<div class="sector-metrics-container">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Invested", f"₹{sector_invested:.2f}")
                with col2:
                    st.metric("Current Value", f"₹{sector_current_value:.2f}")
                with col3:
                    st.metric("Profit/Loss", f"₹{sector_pl:.2f}")
                with col4:
                    st.metric("Companies", len(sector_companies))
                st.markdown('</div>', unsafe_allow_html=True)
                
                data = []
                for company in sector_companies:
                    current_price = get_current_stock_price(company["ticker"])
                    day_return, day_return_msg = get_today_return(company["ticker"])
                    
                    buy_price = company.get("buy_price", 0)
                    shares = company.get("shares", 0)
                    total_invested = company.get("total_invested", buy_price * shares)
                    purchase_date = company.get("purchase_date", "N/A")
                    is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))
                    
                    pl_data = None
                    if current_price and shares > 0:
                        pl_data = calculate_profit_loss(total_invested / shares if shares > 0 else 0, shares, current_price)
                        sector_current_value += pl_data["current_value"] if pl_data else 0
                        sector_pl += pl_data["profit_loss"] if pl_data else 0
                    
                    currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                    ticker_suffix = "NS" if company["ticker"].endswith(".NS") else "BO" if company["ticker"].endswith(".BO") else "Other"
                    
                    company_data = {
                        "Company": company["name"],
                        "Ticker": company["ticker"],
                        "Type": "IPO" if is_ipo else "Regular",
                        "Purchase Date": purchase_date,
                        "Current Price": f"{currency_symbol}{current_price:.2f}" if current_price else "N/A",
                        "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                        "Shares": shares,
                        "Day Change": f"{day_return}%" if day_return is not None else f"N/A ({day_return_msg})",
                        "Invested": f"{currency_symbol}{total_invested:.2f}",
                        "Ticker Suffix": ticker_suffix,
                        "ID": company["id"],
                        "Actions": ""
                    }
                    
                    if pl_data:
                        company_data.update({
                            "Current Value": f"{currency_symbol}{pl_data['current_value']:.2f}",
                            "P/L": f"{currency_symbol}{pl_data['profit_loss']:.2f}",
                            "P/L %": f"{pl_data['profit_loss_percent']:.2f}%"
                        })
                    else:
                        company_data.update({
                            "Current Value": "N/A",
                            "P/L": "N/A",
                            "P/L %": "N/A"
                        })
                        
                    data.append(company_data)
                
                # Update sector metrics
                st.markdown('<div class="sector-metrics-container">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Invested", f"₹{sector_invested:.2f}")
                with col2:
                    st.metric("Current Value", f"₹{sector_current_value:.2f}")
                with col3:
                    pl_label = "Profit" if sector_pl >= 0 else "Loss"
                    sector_pl_pct = (sector_pl / sector_invested * 100) if sector_invested > 0 else 0
                    st.metric(pl_label, f"₹{abs(sector_pl):.2f}", f"{sector_pl_pct:.2f}%", 
                              delta_color="normal" if sector_pl >= 0 else "inverse")
                with col4:
                    st.metric("Companies", len(sector_companies))
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Companies table
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                st.subheader("Companies in Sector")
                # Header row
                st.markdown('<div class="table-row">', unsafe_allow_html=True)
                cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
                headers = ["Company", "Ticker", "Type", "Purchase Date", "Current Price", "Buy Price", 
                           "Shares", "Day Change", "Current Value", "P/L", "Actions"]
                for col, header in zip(cols, headers):
                    with col:
                        st.markdown(f'<div class="table-cell"><b>{header}</b></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Data rows
                for company_data in data:
                    is_ipo = company_data["Type"] == "IPO"
                    st.markdown('<div class="table-row">', unsafe_allow_html=True)
                    cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
                    with cols[0]:
                        st.markdown(
                            f'<div class="table-cell"><span style="color: {"#00FF00" if is_ipo else "#1E3A8A"}; font-weight: {"bold" if is_ipo else "normal"};">{company_data["Company"]}</span></div>',
                            unsafe_allow_html=True
                        )
                    with cols[1]:
                        st.markdown(f'<div class="table-cell">{company_data["Ticker"]}</div>', unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown(f'<div class="table-cell">{company_data["Type"]}</div>', unsafe_allow_html=True)
                    with cols[3]:
                        st.markdown(f'<div class="table-cell">{company_data["Purchase Date"]}</div>', unsafe_allow_html=True)
                    with cols[4]:
                        st.markdown(f'<div class="table-cell">{company_data["Current Price"]}</div>', unsafe_allow_html=True)
                    with cols[5]:
                        st.markdown(f'<div class="table-cell">{company_data["Buy Price"]}</div>', unsafe_allow_html=True)
                    with cols[6]:
                        st.markdown(f'<div class="table-cell">{company_data["Shares"]}</div>', unsafe_allow_html=True)
                    with cols[7]:
                        st.markdown(f'<div class="table-cell">{company_data["Day Change"]}</div>', unsafe_allow_html=True)
                    with cols[8]:
                        st.markdown(f'<div class="table-cell">{company_data["Current Value"]}</div>', unsafe_allow_html=True)
                    with cols[9]:
                        st.markdown(f'<div class="table-cell">{company_data["P/L"]}</div>', unsafe_allow_html=True)
                    with cols[10]:
                        st.markdown('<div class="table-cell">', unsafe_allow_html=True)
                        col_edit, col_remove, col_view = st.columns(3)
                        with col_edit:
                            if st.button("Edit", key=f"edit_{company_data['ID']}"):
                                toggle_edit_company(company_data["ID"])
                                st.rerun()
                        with col_remove:
                            if st.button("Remove", key=f"remove_{company_data['ID']}"):
                                st.session_state.data["companies"] = [
                                    c for c in st.session_state.data["companies"] if c["id"] != company_data["ID"]
                                ]
                                st.session_state.data["transactions"] = [
                                    t for t in st.session_state.data["transactions"] if t["company_id"] != company_data["ID"]
                                ]
                                save_data(st.session_state.data)
                                st.success(f"Company '{company_data['Company']}' removed successfully!")
                                st.rerun()
                        with col_view:
                            if st.button("View", key=f"view_details_{company_data['ID']}"):
                                st.session_state.view_company_details = company_data["ID"]
                                st.session_state.selected_sector_for_view = None
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# Main Page (Home)
if not any([
    st.session_state.add_sector_clicked,
    st.session_state.add_company_clicked,
    st.session_state.add_ipo_clicked,
    st.session_state.view_mode,
    st.session_state.show_high_return,
    st.session_state.show_hx_cat,
    st.session_state.show_invest_companies,
    st.session_state.show_visualize_companies,
    st.session_state.show_journal_ledger,
    st.session_state.edit_company
]):
    st.header("Portfolio Dashboard")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        # Debug buttons
        if st.button("Debug: List Tickers"):
            st.write([c["ticker"] for c in st.session_state.data["companies"]])
        if st.button("Debug: Clear Cache"):
            st.session_state.return_cache = {}
            st.rerun()
        
        # Prepare data for all components
        component_data = []
        for company in st.session_state.data["companies"]:
            day_return, day_return_msg = get_today_return(company["ticker"])
            current_price = get_current_stock_price(company["ticker"])
            buy_price = company.get("buy_price", 0)
            shares = company.get("shares", 0)
            total_invested = company.get("total_invested", buy_price * shares)
            currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
            
            pl_data = calculate_profit_loss(buy_price, shares, current_price) if current_price and shares > 0 else None
            
            company_data = {
                "Company": company["name"],
                "Sector": company["sector"],
                "Day Change (%)": day_return if day_return is not None else None,
                "Day Change Display": f"{day_return:.2f}%" if day_return is not None else f"N/A ({day_return_msg})",
                "P/L": pl_data["profit_loss"] if pl_data else 0,
                "P/L %": pl_data["profit_loss_percent"] if pl_data else 0,
                "Invested Amount": total_invested,
                "Shares": shares,
                "HX-CAT": company.get("hx_cat", False),
                "Formatted P/L": f"{currency_symbol}{pl_data['profit_loss']:.2f}" if pl_data else "N/A",
                "Formatted Invested": f"{currency_symbol}{total_invested:.2f}"
            }
            if day_return is None:
                print(f"Day Change N/A for {company['ticker']}: {day_return_msg}")
            component_data.append(company_data)
        
        df_all = pd.DataFrame(component_data)
        
        # Component 1: Top 5 Companies by High Day Change (shares > 0)
        with st.container():
            st.subheader("Top 5 Companies by High Day Change (Holding)")
            df_filtered = df_all[df_all["Shares"] > 0]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "Formatted P/L", "P/L %", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data and holdings.")
        
        # Component 2: Top 5 Companies by High P/L% (shares > 0)
        with st.container():
            st.subheader("Top 5 Companies by High P/L% (Holding)")
            df_filtered = df_all[df_all["Shares"] > 0]
            if not df_filtered.empty and df_filtered["P/L %"].notna().any():
                df_sorted = df_filtered.sort_values(by="P/L %", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid P/L% data and holdings.")
        
        # Component 3: Top 5 HX-Category Companies by High Day Change
        with st.container():
            st.subheader("Top 5 HX-Category Companies by High Day Change")
            df_filtered = df_all[df_all["HX-CAT"] == True]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No HX-Category companies with valid day change data.")
        
        # Component 4: Top 5 HX-Category Companies by Low Day Change
        with st.container():
            st.subheader("Top 5 HX-Category Companies by Low Day Change")
            df_filtered = df_all[df_all["HX-CAT"] == True]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=True).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No HX-Category companies with valid day change data.")
        
        # Component 5: Top 10 Companies by High Day Change
        with st.container():
            st.subheader("Top 10 Companies by High Day Change (All)")
            if not df_all.empty and df_all["Day Change (%)"].notna().any():
                df_sorted = df_all.sort_values(by="Day Change (%)", ascending=False).head(10)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data.")
        
        # Component 6: Top 10 Companies by Low Day Change
        with st.container():
            st.subheader("Top 10 Companies by Low Day Change (All)")
            if not df_all.empty and df_all["Day Change (%)"].notna().any():
                df_sorted = df_all.sort_values(by="Day Change (%)", ascending=True).head(10)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data.")