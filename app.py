import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import datetime
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
import uuid
import time

# Set page title and configuration
st.set_page_config(page_title="Sector-based Stock Tracker", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

# Define functions for data management
def save_data(data):
    """Save data to a JSON file"""
    with open('stock_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
def load_data():
    """Load data from JSON file or initialize empty structure"""
    if os.path.exists('stock_data.json'):
        with open('stock_data.json', 'r') as f:
            data = json.load(f)
        # Ensure all companies have an 'id' and 'total_invested' field
        for company in data.get("companies", []):
            if "id" not in company:
                company["id"] = str(uuid.uuid4())
            # Initialize total_invested if missing
            if "total_invested" not in company:
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                company["total_invested"] = buy_price * shares
            # Initialize profit/loss fields if missing
            if "profit_until_now" not in company:
                company["profit_until_now"] = 0.0
            if "loss_until_now" not in company:
                company["loss_until_now"] = 0.0
            # Initialize transaction for existing companies with shares if none exist
            if company.get("shares", 0) > 0 and company["total_invested"] > 0:
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                total_invested = company["total_invested"]
                if not any(t["company_id"] == company["id"] for t in data.get("transactions", [])):
                    transaction = {
                        "company_id": company["id"],
                        "type": "buy",
                        "amount": total_invested,
                        "shares": shares,
                        "price_per_share": buy_price,
                        "date": company.get("purchase_date", datetime.date.today().strftime("%Y-%m-%d")),
                        "profit_loss": 0.0
                    }
                    data["transactions"] = data.get("transactions", []) + [transaction]
        save_data(data)  # Save updated data
        return data
    else:
        return {
            "sectors": [],
            "companies": [],
            "transactions": []
        }

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
    """Calculate today's return percentage with fallback to previous trading day"""
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
            # Start from today and go back up to 5 days to find the last trading day
            data = stock.history(start=today - timedelta(days=5), end=today + timedelta(days=1), interval="1d")
            
            if len(data) < 1:
                return None, "Not enough data"
            
            # Get today's close
            today_str = today.strftime('%Y-%m-%d')
            today_close = None
            if today_str in data.index.strftime('%Y-%m-%d'):
                today_close = data.loc[today_str]["Close"]
            
            # Find the last available trading day before today
            previous_close = None
            previous_date = None
            for date in data.index[::-1]:
                date_str = date.strftime('%Y-%m-%d')
                if date_str < today_str:
                    previous_close = data.loc[date_str]["Close"]
                    previous_date = date_str
                    break
            
            if today_close is None or previous_close is None:
                return None, "Missing price data"
            
            if previous_close == 0:
                return None, "Invalid data: Zero close price"
            
            return_pct = ((today_close - previous_close) / previous_close) * 100
            return_value = round(return_pct, 2)
            
            # Cache the result
            st.session_state.return_cache[cache_key] = (return_value, f"{previous_date} to {today_str}")
            return return_value, f"{previous_date} to {today_str}"
        
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retrying
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

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
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

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False
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
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
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
    if st.button("View Sectors", key="view_mode_button", 
                 type="primary" if st.session_state.view_mode else "secondary"):
        toggle_view_mode()
with col5:
    if st.button("High Return", key="high_return_button",
                 type="primary" if st.session_state.show_high_return else "secondary"):
        toggle_high_return()
with col6:
    if st.button("Track-HX-CAT", key="hx_cat_button",
                 type="primary" if st.session_state.show_hx_cat else "secondary"):
        toggle_hx_cat()
with col7:
    if st.button("Track_Invest", key="invest_companies_button",
                 type="primary" if st.session_state.show_invest_companies else "secondary"):
        toggle_invest_companies()
with col8:
    if st.button("Visualize Companies", key="visualize_companies_button",
                 type="primary" if st.session_state.show_visualize_companies else "secondary"):
        toggle_visualize_companies()
with col9:
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
            company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc.")
            ticker_code = st.text_input("Ticker Code", placeholder="e.g. AAPL")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"])
            
            buy_price = st.number_input("Buy Price", min_value=0.00, format="%.2f", 
                                       placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=0, step=1, 
                                    placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", 
                                         value=datetime.date.today(),
                                         max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO", ""]
            suffix = st.selectbox("Exchange Suffix", suffix_options, 
                                  index=0, 
                                  help=".NS for NSE, .BO for BSE, blank for US markets")
            
            move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], 
                                     help="Select Yes to tag as HX-CAT")
            
            submit_company = st.form_submit_button("Add Company")
            
            if submit_company and company_name and ticker_code and buy_price > 0:
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
                            "loss_until_now": 0.0
                        }
                        st.session_state.data["companies"].append(new_company)
                        # Log transaction
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
                st.error("Please fill all required fields with valid values.")

# Edit Company Form
if st.session_state.edit_company:
    company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.edit_company), None)
    if company:
        st.subheader(f"Edit Company: {company['name']}")
        with st.form(f"edit_company_form_{company['id']}"):
            company_name = st.text_input("Company Name", value=company["name"], placeholder="e.g. Apple Inc.")
            ticker_code = st.text_input("Ticker Code", value=company["ticker"].replace(".NS", "").replace(".BO", ""), placeholder="e.g. AAPL")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"], index=st.session_state.data["sectors"].index(company["sector"]))
            
            buy_price = st.number_input("Buy Price", min_value=0.00, format="%.2f", value=float(company["buy_price"]), placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=0, step=1, value=int(company["shares"]), placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", value=datetime.datetime.strptime(company["purchase_date"], "%Y-%m-%d").date(), max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO", ""]
            current_suffix = ".NS" if company["ticker"].endswith(".NS") else ".BO" if company["ticker"].endswith(".BO") else ""
            suffix = st.selectbox("Exchange Suffix", suffix_options, index=suffix_options.index(current_suffix), help=".NS for NSE, .BO for BSE, blank for US markets")
            
            move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], index=1 if company["hx_cat"] else 0, help="Select Yes to tag as HX-CAT")
            
            col1, col2 = st.form_submit_button("Update Company"), st.form_submit_button("Cancel")
            
            if col1 and company_name and ticker_code and buy_price > 0:
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
                            "total_invested": float(buy_price) * int(shares)
                        })
                        # Update transaction if exists, or create new one
                        existing_transaction = next((t for t in st.session_state.data["transactions"] if t["company_id"] == company["id"] and t["type"] == "buy"), None)
                        if existing_transaction:
                            existing_transaction.update({
                                "amount": company["total_invested"],
                                "shares": company["shares"],
                                "price_per_share": company["buy_price"],
                                "date": company["purchase_date"],
                                "profit_loss": 0.0
                            })
                        else:
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
                st.error("Please fill all required fields with valid values.")
            elif col2:
                st.session_state.edit_company = None
                st.rerun()

# Journal & Ledger Section
if st.session_state.show_journal_ledger:
    st.header("Journal & Ledger")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
    else:
        data = []
        for company in st.session_state.data["companies"]:
            total_invested = company.get("total_invested", 0)
            if total_invested > 1:
                shares = company.get("shares", 0)
                avg_share_price = total_invested / shares if shares > 0 else 0
                current_price = get_current_stock_price(company["ticker"])
                currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                company_data = {
                    "Company": company["name"],
                    "Total Invested": f"{currency_symbol}{total_invested:.2f}",
                    "Total No. of Shares Holding": shares,
                    "Profit Until Now": f"{currency_symbol}{company.get('profit_until_now', 0):.2f}",
                    "Loss Until Now": f"{currency_symbol}{company.get('loss_until_now', 0):.2f}",
                    "Each Share Price": f"{currency_symbol}{avg_share_price:.2f}",
                    "Current Price": f"{currency_symbol}{current_price:.2f}" if current_price else "N/A",
                    "ID": company["id"]
                }
                data.append(company_data)
        
        if not data:
            st.info("No companies with total invested amount greater than ₹1 found.")
        else:
            df = pd.DataFrame(data)
            st.subheader("Investment Ledger")
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
            
            st.subheader("Manage Transactions")
            selected_company = st.selectbox("Select Company", options=[d["Company"] for d in data], key="ledger_company")
            selected_company_data = next((d for d in data if d["Company"] == selected_company), None)
            
            if selected_company_data:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Sold Shares", key=f"sell_{selected_company_data['ID']}"):
                        st.session_state[f"sell_form_{selected_company_data['ID']}"] = True
                with col2:
                    if st.button("Invested More", key=f"invest_{selected_company_data['ID']}"):
                        st.session_state[f"invest_form_{selected_company_data['ID']}"] = True
                
                # Sell Shares Form
                if st.session_state.get(f"sell_form_{selected_company_data['ID']}", False):
                    with st.form(f"sell_shares_form_{selected_company_data['ID']}"):
                        shares_sold = st.number_input("Number of Shares Sold", min_value=1, max_value=selected_company_data["Total No. of Shares Holding"], step=1)
                        sell_price_per_share = st.number_input("Sell Price per Share", min_value=0.00, format="%.2f")
                        total_sold_amt = shares_sold * sell_price_per_share
                        st.write(f"Total Sale Value: {currency_symbol}{total_sold_amt:.2f}")
                        submit_sell = st.form_submit_button("Confirm Sale")
                        
                        if submit_sell and total_sold_amt > 0 and shares_sold > 0:
                            company = next((c for c in st.session_state.data["companies"] if c["id"] == selected_company_data["ID"]), None)
                            if company:
                                # Calculate average buy price
                                current_shares = company.get("shares", 0)
                                current_total_invested = company.get("total_invested", 0)
                                avg_buy_price = current_total_invested / current_shares if current_shares > 0 else 0
                                
                                # Calculate profit/loss for sold shares
                                pl = (sell_price_per_share - avg_buy_price) * shares_sold
                                
                                # Update profit/loss fields
                                if pl >= 0:
                                    company["profit_until_now"] = company.get("profit_until_now", 0) + pl
                                    company["loss_until_now"] = company.get("loss_until_now", 0)
                                else:
                                    company["loss_until_now"] = company.get("loss_until_now", 0) + abs(pl)
                                    company["profit_until_now"] = company.get("profit_until_now", 0)
                                
                                # Update shares and total invested
                                cost_of_sold_shares = avg_buy_price * shares_sold
                                company["shares"] = current_shares - shares_sold
                                company["total_invested"] = current_total_invested - cost_of_sold_shares
                                
                                # Update buy price for remaining shares
                                if company["shares"] > 0:
                                    company["buy_price"] = company["total_invested"] / company["shares"]
                                else:
                                    company["buy_price"] = 0
                                    company["total_invested"] = 0
                                    company["profit_until_now"] = 0
                                    company["loss_until_now"] = 0
                                
                                # Log transaction
                                transaction = {
                                    "company_id": company["id"],
                                    "type": "sell",
                                    "amount": total_sold_amt,
                                    "shares": shares_sold,
                                    "price_per_share": sell_price_per_share,
                                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                                    "profit_loss": pl
                                }
                                st.session_state.data["transactions"].append(transaction)
                                
                                save_data(st.session_state.data)
                                st.success(f"Sold {shares_sold} shares of {selected_company} for {currency_symbol}{total_sold_amt:.2f}!")
                                st.session_state[f"sell_form_{selected_company_data['ID']}"] = False
                                st.rerun()
                
                # Invest More Form
                if st.session_state.get(f"invest_form_{selected_company_data['ID']}", False):
                    with st.form(f"invest_more_form_{selected_company_data['ID']}"):
                        new_shares = st.number_input("Total Newly Bought Shares", min_value=1, step=1)
                        buy_price_per_share = st.number_input("Buy Price per Share", min_value=0.00, format="%.2f")
                        total_new_amount = new_shares * buy_price_per_share
                        st.write(f"Total Investment: {currency_symbol}{total_new_amount:.2f}")
                        submit_invest = st.form_submit_button("Confirm Investment")
                        
                        if submit_invest and total_new_amount > 0 and new_shares > 0:
                            company = next((c for c in st.session_state.data["companies"] if c["id"] == selected_company_data["ID"]), None)
                            if company:
                                # Initialize total_invested if missing
                                if "total_invested" not in company:
                                    company["total_invested"] = 0.0
                                
                                # Update total invested and shares
                                company["total_invested"] += total_new_amount
                                company["shares"] = company.get("shares", 0) + new_shares
                                
                                # Update average buy price
                                company["buy_price"] = company["total_invested"] / company["shares"] if company["shares"] > 0 else 0
                                
                                # Log transaction
                                transaction = {
                                    "company_id": company["id"],
                                    "type": "buy",
                                    "amount": total_new_amount,
                                    "shares": new_shares,
                                    "price_per_share": buy_price_per_share,
                                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                                    "profit_loss": 0.0
                                }
                                st.session_state.data["transactions"].append(transaction)
                                
                                save_data(st.session_state.data)
                                st.success(f"Invested {currency_symbol}{total_new_amount:.2f} in {new_shares} shares of {selected_company}!")
                                st.session_state[f"invest_form_{selected_company_data['ID']}"] = False
                                st.rerun()

# Visualize Companies Section
if st.session_state.show_visualize_companies:
    st.header("Company Investment Analysis")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
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
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
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
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
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
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
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
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
    else:
        if st.session_state.selected_sector_for_view is None:
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
                sector_daily_change = 0
                
                data = []
                for company in sector_companies:
                    current_price = get_current_stock_price(company["ticker"])
                    day_return, day_period = get_today_return(company["ticker"])
                    
                    buy_price = company.get("buy_price", 0)
                    shares = company.get("shares", 0)
                    total_invested = company.get("total_invested", buy_price * shares)
                    purchase_date = company.get("purchase_date", "N/A")
                    
                    pl_data = None
                    if current_price and shares > 0:
                        pl_data = calculate_profit_loss(total_invested / shares if shares > 0 else 0, shares, current_price)
                        sector_current_value += pl_data["current_value"] if pl_data else 0
                    
                    currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                    
                    company_data = {
                        "Company": company["name"],
                        "Ticker": company["ticker"],
                        "Purchase Date": purchase_date,
                        "Current Price": f"{currency_symbol}{current_price:.2f}" if current_price else "N/A",
                        "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                        "Shares": shares,
                        "Invested": f"{currency_symbol}{total_invested:.2f}",
                        "Day Change": f"{day_return}%" if day_return is not None else "N/A",
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
                
                sector_pl = sector_current_value - sector_invested
                sector_pl_pct = (sector_pl / sector_invested * 100) if sector_invested > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Invested", f"₹{sector_invested:.2f}")
                with col2:
                    st.metric("Current Value", f"₹{sector_current_value:.2f}")
                with col3:
                    pl_label = "Profit" if sector_pl >= 0 else "Loss"
                    st.metric(pl_label, f"₹{abs(sector_pl):.2f}", 
                             f"{sector_pl_pct:.2f}%", 
                             delta_color="normal" if sector_pl >= 0 else "inverse")
                with col4:
                    st.metric("Holdings", f"{len(sector_companies)} Stocks")
                
                st.subheader(f"Companies in {selected_sector}")
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)

# Main content area - Display stocks by sector
if not any([st.session_state.view_mode, st.session_state.show_high_return, 
            st.session_state.show_hx_cat, st.session_state.show_invest_companies,
            st.session_state.show_visualize_companies, st.session_state.show_journal_ledger,
            st.session_state.edit_company]):
    st.header("Stocks by Sector")

    if st.session_state.data["companies"]:
        total_invested = 0
        total_current_value = 0
        
        for company in st.session_state.data["companies"]:
            total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
            shares = company.get("shares", 0)
            current_price = get_current_stock_price(company["ticker"])
            
            if total_invested_company > 0 and shares > 0 and current_price:
                total_invested += total_invested_company
                current_val = current_price * shares
                total_current_value += current_val
        
        total_profit_loss = total_current_value - total_invested
        total_profit_loss_percent = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        st.subheader("Portfolio Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Invested", f"₹{total_invested:.2f}")
        with col2:
            st.metric("Current Value", f"₹{total_current_value:.2f}")
        with col3:
            pl_label = "Profit" if total_profit_loss >= 0 else "Loss"
            st.metric(pl_label, f"₹{abs(total_profit_loss):.2f}", 
                     f"{total_profit_loss_percent:.2f}%", 
                     delta_color="normal" if total_profit_loss >= 0 else "inverse")
        with col4:
            st.metric("Holdings", f"{len(st.session_state.data['companies'])} Stocks")

    if not st.session_state.data["sectors"]:
        st.info("No sectors added yet. Click 'Add Sector' to get started.")
    elif not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
    else:
        for sector in st.session_state.data["sectors"]:
            sector_companies = [company for company in st.session_state.data["companies"] 
                               if company["sector"] == sector]
            
            if sector_companies:
                sector_invested = sum(company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0)) 
                                     for company in sector_companies)
                
                with st.expander(f"{sector} ({len(sector_companies)} companies)", expanded=True):
                    data = []
                    for company in sector_companies:
                        price = get_current_stock_price(company["ticker"])
                        day_return, day_period = get_today_return(company["ticker"])
                        
                        buy_price = company.get("buy_price", 0)
                        shares = company.get("shares", 0)
                        total_invested = company.get("total_invested", buy_price * shares)
                        purchase_date = company.get("purchase_date", "N/A")
                        
                        pl_data = None
                        if price and shares > 0:
                            pl_data = calculate_profit_loss(total_invested / shares if shares > 0 else 0, shares, price)
                        
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        
                        company_data = {
                            "Company": company["name"],
                            "Ticker": company["ticker"],
                            "Purchase Date": purchase_date,
                            "Current Price": f"{currency_symbol}{price:.2f}" if price else "N/A",
                            "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                            "Shares": shares,
                            "Day Change": f"{day_return}%" if day_return is not None else "N/A",
                            "Invested": f"{currency_symbol}{total_invested:.2f}",
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
                            
                        data.append(company_data)
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col2:
                        company_to_delete = st.selectbox(f"Select company to remove from {sector}", 
                                                        [c["name"] for c in sector_companies],
                                                        key=f"delete_{sector}")
                        if st.button("Remove Company", key=f"remove_{sector}"):
                            company_index = next((i for i, c in enumerate(st.session_state.data["companies"])
                                                if c["name"] == company_to_delete), None)
                            if company_index is not None:
                                st.session_state.data["companies"].pop(company_index)
                                save_data(st.session_state.data)
                                st.success(f"Removed {company_to_delete} from tracking")
                                st.rerun()
                    with col3:
                        company_to_edit = st.selectbox(f"Select company to edit in {sector}", 
                                                      [c["name"] for c in sector_companies],
                                                      key=f"edit_select_{sector}")
                        if st.button("Edit Company", key=f"edit_{sector}"):
                            company_id = next(c["id"] for c in sector_companies if c["name"] == company_to_edit)
                            toggle_edit_company(company_id)
                            st.rerun()

# Sector Management
st.sidebar.header("Manage Sectors")
if st.session_state.data["sectors"]:
    sector_to_delete = st.sidebar.selectbox("Select sector to delete", st.session_state.data["sectors"])
    if st.sidebar.button("Delete Sector"):
        companies_in_sector = [c for c in st.session_state.data["companies"] if c["sector"] == sector_to_delete]
        if companies_in_sector:
            st.sidebar.error(f"Cannot delete sector '{sector_to_delete}' because it contains {len(companies_in_sector)} companies. Remove them first.")
        else:
            st.session_state.data["sectors"].remove(sector_to_delete)
            save_data(st.session_state.data)
            st.sidebar.success(f"Deleted sector '{sector_to_delete}'")
            st.rerun()
else:
    st.sidebar.info("No sectors to manage")

# Current date display
current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
st.sidebar.markdown(f"**Today's Date:** {current_date}")

# About section in sidebar
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("""
This app allows you to track stock prices by sector.
1. Add sectors to organize your stocks
2. Add companies with their ticker codes
3. View current prices and profit/loss information
4. Monitor daily returns and overall portfolio performance
5. Visualize investment weightage by sector or market cap
6. Manage transactions with Journal & Ledger
""")