import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import datetime
from datetime import timedelta

# Set page title and configuration
st.set_page_config(page_title="Sector-based Stock Tracker", layout="wide")

# Custom CSS for blue and white theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #F5F8FF;
        color: #1E3A8A;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1E3A8A;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: white;
    }
    .stButton>button:focus {
        background-color: #1E40AF;
        color: white;
    }
    
    /* Primary button (View Mode, High Return when active) */
    .stButton>button[kind="primary"] {
        background-color: #1E40AF;
        color: white;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1E3A8A;
        color: white;
    }
    
    /* Form labels */
    .stForm label, .stTextInput label, .stNumberInput label, 
    .stDateInput label, .stSelectbox label {
        color: #1E3A8A !important;
    }
    
    /* Text inputs and select boxes */
    .stTextInput>div>input,
    .stNumberInput>div>input,
    .stDateInput>div>input,
    .stSelectbox>div>div>select {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
        border-radius: 5px;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        width: 100%;
    }
    .stDataFrame table {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
        border-collapse: collapse;
    }
    .stDataFrame th {
        background-color: #3B82F6;
        color: white;
        border: 1px solid #93C5FD;
        padding: 8px;
    }
    .stDataFrame td {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
        padding: 8px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #EFF6FF;
    }
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stInfo,
    .css-1d391kg .stError,
    .css-1d391kg .stSuccess {
        color: #1E3A8A;
    }
    
    /* Info, Warning, Error, Success messages */
    .stInfo, .stWarning, .stError, .stSuccess {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
    }
    
    /* Metrics */
    .stMetric {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
        border-radius: 5px;
    }
    
    /* Expander */
    .streamlit-expander {
        background-color: white;
        color: #1E3A8A;
        border: 1px solid #93C5FD;
        border-radius: 5px;
    }
    
    /* Horizontal line */
    hr {
        border-color: #93C5FD;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

# Define functions for data management
def save_data(data):
    """Save data to a JSON file"""
    with open('stock_data.json', 'w') as f:
        json.dump(data, f)
    
def load_data():
    """Load data from JSON file or initialize empty structure"""
    if os.path.exists('stock_data.json'):
        with open('stock_data.json', 'r') as f:
            return json.load(f)
    else:
        return {"sectors": [], "companies": []}

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
    """Calculate today's return percentage for a stock"""
    try:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period="7d", interval="1d")
        
        if len(data) < 2:
            return None, "Not enough data"
            
        yesterday_close = data["Close"].iloc[-2]
        today_close = data["Close"].iloc[-1]
        
        return_pct = ((today_close - yesterday_close) / yesterday_close) * 100
        return_value = round(return_pct, 2)
        
        today_date = data.index[-1].strftime("%Y-%m-%d")
        yesterday_date = data.index[-2].strftime("%Y-%m-%d")
        
        return return_value, f"{yesterday_date} to {today_date}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def calculate_profit_loss(buy_price, shares, current_price):
    """Calculate profit/loss for a position"""
    if buy_price and shares and current_price:
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

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False

def toggle_view_mode():
    st.session_state.view_mode = not st.session_state.view_mode
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    if st.session_state.view_mode:
        st.session_state.selected_sector_for_view = None

def toggle_high_return():
    st.session_state.show_high_return = not st.session_state.show_high_return
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    if st.session_state.show_high_return:
        st.session_state.high_return_sector = "All Sectors"

def toggle_hx_cat():
    st.session_state.show_hx_cat = not st.session_state.show_hx_cat
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_invest_companies = False

def toggle_invest_companies():
    st.session_state.show_invest_companies = not st.session_state.show_invest_companies
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    if st.session_state.show_invest_companies:
        st.session_state.invest_companies_sector = "All Sectors"

def set_selected_sector(sector):
    st.session_state.selected_sector_for_view = sector

def go_to_home():
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.selected_sector_for_view = None
    st.rerun()

# App title and description
st.title("📈 HOOX Companywise Tracker & Analysis")
st.markdown("Track stock prices organized by business sectors")

# Action buttons at the top
st.markdown("### Actions")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
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
                            "name": company_name,
                            "ticker": full_ticker,
                            "sector": selected_sector,
                            "buy_price": float(buy_price),
                            "shares": int(shares),
                            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                            "hx_cat": move_to_hx == "Yes"
                        }
                        st.session_state.data["companies"].append(new_company)
                        save_data(st.session_state.data)
                        st.success(f"Company '{company_name}' added successfully!")
                        st.session_state.add_company_clicked = False
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
            elif submit_company:
                st.error("Please fill all required fields with valid values.")

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
            if company["shares"] > 0 and (selected_sector == "All Sectors" or company["sector"] == selected_sector):
                day_return, _ = get_today_return(company["ticker"])
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                invested = buy_price * shares
                currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                
                company_data = {
                    "Company": company["name"],
                    "Sector": company["sector"],
                    "Ticker": company["ticker"],
                    "Purchase Date": company.get("purchase_date", "N/A"),
                    "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                    "Shares": shares,
                    "Invested": f"{currency_symbol}{invested:.2f}",
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
                        sector_invested = sum(c.get("buy_price", 0) * c.get("shares", 0) for c in sector_companies)
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
                sector_invested = sum(c.get("buy_price", 0) * c.get("shares", 0) for c in sector_companies)
                sector_current_value = 0
                sector_daily_change = 0
                
                data = []
                for company in sector_companies:
                    current_price = get_current_stock_price(company["ticker"])
                    day_return, day_period = get_today_return(company["ticker"])
                    
                    buy_price = company.get("buy_price", 0)
                    shares = company.get("shares", 0)
                    purchase_date = company.get("purchase_date", "N/A")
                    
                    pl_data = None
                    if current_price:
                        pl_data = calculate_profit_loss(buy_price, shares, current_price)
                        sector_current_value += pl_data["current_value"]
                    
                    currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                    
                    company_data = {
                        "Company": company["name"],
                        "Ticker": company["ticker"],
                        "Purchase Date": purchase_date,
                        "Current Price": f"{currency_symbol}{current_price}" if current_price else "N/A",
                        "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                        "Shares": shares,
                        "Invested": f"{currency_symbol}{buy_price * shares:.2f}",
                        "Day Change": f"{day_return}%" if day_return is not None else "N/A",
                    }
                    
                    if pl_data:
                        company_data.update({
                            "Current Value": f"{currency_symbol}{pl_data['current_value']}",
                            "P/L": f"{currency_symbol}{pl_data['profit_loss']}",
                            "P/L %": f"{pl_data['profit_loss_percent']}%"
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

# Main content area - Display stocks by sector (when not in view mode or high return)
if not st.session_state.view_mode and not st.session_state.show_high_return and not st.session_state.show_hx_cat and not st.session_state.show_invest_companies:
    st.header("Stocks by Sector")

    if st.session_state.data["companies"]:
        total_invested = 0
        total_current_value = 0
        
        for company in st.session_state.data["companies"]:
            buy_price = company.get("buy_price", 0)
            shares = company.get("shares", 0)
            current_price = get_current_stock_price(company["ticker"])
            
            if buy_price and shares and current_price:
                invested = buy_price * shares
                current_val = current_price * shares
                total_invested += invested
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
                sector_invested = sum(company.get("buy_price", 0) * company.get("shares", 0) 
                                     for company in sector_companies)
                
                with st.expander(f"{sector} ({len(sector_companies)} companies)", expanded=True):
                    data = []
                    for company in sector_companies:
                        price = get_current_stock_price(company["ticker"])
                        day_return, day_period = get_today_return(company["ticker"])
                        
                        buy_price = company.get("buy_price", 0)
                        shares = company.get("shares", 0)
                        purchase_date = company.get("purchase_date", "N/A")
                        
                        pl_data = None
                        if price:
                            pl_data = calculate_profit_loss(buy_price, shares, price)
                        
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        
                        company_data = {
                            "Company": company["name"],
                            "Ticker": company["ticker"],
                            "Purchase Date": purchase_date,
                            "Current Price": f"{currency_symbol}{price}" if price else "N/A",
                            "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                            "Shares": shares,
                            "Day Change": f"{day_return}%" if day_return is not None else "N/A",
                            "Invested": f"{currency_symbol}{buy_price * shares:.2f}",
                        }
                        
                        if pl_data:
                            company_data.update({
                                "Current Value": f"{currency_symbol}{pl_data['current_value']}",
                                "P/L": f"{currency_symbol}{pl_data['profit_loss']}",
                                "P/L %": f"{pl_data['profit_loss_percent']}%"
                            })
                        else:
                            company_data.update({
                                "Current Value": "N/A",
                                "P/L": "N/A",
                                "P/L %": "N/A"
                            })
                            
                        data.append(company_data)
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    
                    col1, col2 = st.columns([3, 1])
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
""")