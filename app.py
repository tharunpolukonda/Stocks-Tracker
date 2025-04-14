import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import datetime
from datetime import timedelta

# Set page title and configuration
st.set_page_config(page_title="Sector-based Stock Tracker", layout="wide")

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
        # Fetch the last 7 days of data to ensure we have enough history
        data = stock.history(period="7d", interval="1d")
        
        if len(data) < 2:
            return None, "Not enough data"
            
        # Get the latest two trading days
        yesterday_close = data["Close"].iloc[-2]
        today_close = data["Close"].iloc[-1]
        
        # Calculate return percentage
        return_pct = ((today_close - yesterday_close) / yesterday_close) * 100
        return_value = round(return_pct, 2)
        
        # Get the dates for display
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

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False

def toggle_view_mode():
    st.session_state.view_mode = not st.session_state.view_mode
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.show_high_return = False
    if st.session_state.view_mode:
        st.session_state.selected_sector_for_view = None

def toggle_high_return():
    st.session_state.show_high_return = not st.session_state.show_high_return
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False

def set_selected_sector(sector):
    st.session_state.selected_sector_for_view = sector

# App title and description
st.title("📈 Sector-based Stock Tracker")
st.markdown("Track stock prices organized by business sectors")

# Action buttons in sidebar
st.sidebar.header("Actions")
col1, col2, col3, col4 = st.sidebar.columns(4)
with col1:
    st.button("Add Sector", on_click=toggle_add_sector, key="add_sector_button")
with col2:
    st.button("Add Company", on_click=toggle_add_company, key="add_company_button")
with col3:
    st.button("View Mode", on_click=toggle_view_mode, key="view_mode_button", 
             type="primary" if st.session_state.view_mode else "secondary")
with col4:
    st.button("High Return", on_click=toggle_high_return, key="high_return_button",
             type="primary" if st.session_state.show_high_return else "secondary")

# Add Sector Form
if st.session_state.add_sector_clicked:
    st.sidebar.subheader("Add New Sector")
    with st.sidebar.form("add_sector_form"):
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
    st.sidebar.subheader("Add Company to Track")
    
    if not st.session_state.data["sectors"]:
        st.sidebar.warning("Please add at least one sector first!")
    else:
        with st.sidebar.form("add_company_form"):
            company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc.")
            ticker_code = st.text_input("Ticker Code", placeholder="e.g. AAPL")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"])
            
            buy_price = st.number_input("Buy Price", min_value=0.01, format="%.2f", 
                                       placeholder="Enter your purchase price")
            shares = st.number_input("Number of Shares", min_value=1, step=1, 
                                    placeholder="Enter number of shares bought")
            
            purchase_date = st.date_input("Purchase Date", 
                                         value=datetime.date.today(),
                                         max_value=datetime.date.today())
            
            suffix_options = [".NS", ".BO", "", ".L", ".DE"]
            suffix = st.selectbox("Exchange Suffix", suffix_options, 
                                  index=0, 
                                  help=".NS for NSE, .BO for BSE, blank for US markets")
            
            submit_company = st.form_submit_button("Add Company")
            
            if submit_company and company_name and ticker_code and buy_price > 0 and shares > 0:
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
                            "purchase_date": purchase_date.strftime("%Y-%m-%d")
                        }
                        st.session_state.data["companies"].append(new_company)
                        save_data(st.session_state.data)
                        st.success(f"Company '{company_name}' added successfully!")
                        st.session_state.add_company_clicked = False
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
            elif submit_company:
                st.error("Please fill all fields with valid values.")

# High Return Section
if st.session_state.show_high_return:
    st.header("High Return Stocks")
    
    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
    else:
        # Sector filter dropdown
        sectors = ["All Sectors"] + st.session_state.data["sectors"]
        selected_sector = st.selectbox("Filter by Sector", sectors, key="high_return_sector_filter")
        
        # Collect data for companies
        data = []
        for company in st.session_state.data["companies"]:
            if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                day_return, _ = get_today_return(company["ticker"])
                if day_return is not None:  # Only include companies with valid day return
                    data.append({
                        "Company": company["name"],
                        "Sector": company["sector"],
                        "Day Change (%)": day_return
                    })
        
        if not data:
            st.info(f"No companies with valid data found for {selected_sector}.")
        else:
            # Create DataFrame and sort by Day Change in descending order
            df = pd.DataFrame(data)
            df = df.sort_values(by="Day Change (%)", ascending=False)
            
            # Reset index to make it clean
            df = df.reset_index(drop=True)
            
            # Display the table
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
if not st.session_state.view_mode and not st.session_state.show_high_return:
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