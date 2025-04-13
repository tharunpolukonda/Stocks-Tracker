import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os

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

# Initialize session state for managing app state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
    
if 'add_sector_clicked' not in st.session_state:
    st.session_state.add_sector_clicked = False
    
if 'add_company_clicked' not in st.session_state:
    st.session_state.add_company_clicked = False

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
    st.session_state.add_company_clicked = False

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False

# App title and description
st.title("📈 Sector-based Stock Tracker")
st.markdown("Track stock prices organized by business sectors")

# Action buttons in sidebar
st.sidebar.header("Actions")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.button("Add Sector", on_click=toggle_add_sector, key="add_sector_button")
with col2:
    st.button("Add Company", on_click=toggle_add_company, key="add_company_button")

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
    
    # Only show form if sectors exist
    if not st.session_state.data["sectors"]:
        st.sidebar.warning("Please add at least one sector first!")
    else:
        with st.sidebar.form("add_company_form"):
            company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc.")
            ticker_code = st.text_input("Ticker Code", placeholder="e.g. AAPL")
            selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"])
            
            suffix_options = [".NS", ".BO", "" , ".L", ".DE"]
            suffix = st.selectbox("Exchange Suffix", suffix_options, 
                                  index=0, 
                                  help=".NS for NSE, .BO for BSE, blank for US markets")
            
            submit_company = st.form_submit_button("Add Company")
            
            if submit_company and company_name and ticker_code:
                full_ticker = f"{ticker_code}{suffix}"
                
                # Check if company with this ticker already exists
                existing_tickers = [company["ticker"] for company in st.session_state.data["companies"]]
                if full_ticker in existing_tickers:
                    st.error(f"Company with ticker '{full_ticker}' already exists!")
                else:
                    # Verify that the ticker is valid by trying to get the price
                    test_price = get_current_stock_price(full_ticker)
                    if test_price is not None:
                        new_company = {
                            "name": company_name,
                            "ticker": full_ticker,
                            "sector": selected_sector
                        }
                        st.session_state.data["companies"].append(new_company)
                        save_data(st.session_state.data)
                        st.success(f"Company '{company_name}' added successfully!")
                        st.session_state.add_company_clicked = False
                        st.rerun()
                    else:
                        st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")

# Main content area - Display stocks by sector
st.header("Stocks by Sector")

if not st.session_state.data["sectors"]:
    st.info("No sectors added yet. Click 'Add Sector' to get started.")
elif not st.session_state.data["companies"]:
    st.info("No companies added yet. Click 'Add Company' to start tracking stocks.")
else:
    # Group companies by sector
    for sector in st.session_state.data["sectors"]:
        sector_companies = [company for company in st.session_state.data["companies"] 
                           if company["sector"] == sector]
        
        if sector_companies:
            with st.expander(f"{sector} ({len(sector_companies)} companies)", expanded=True):
                # Create a dataframe for this sector's companies
                data = []
                for company in sector_companies:
                    price = get_current_stock_price(company["ticker"])
                    data.append({
                        "Company": company["name"],
                        "Ticker": company["ticker"],
                        "Current Price": f"₹{price}" if price and company["ticker"].endswith(('.NS', '.BO')) 
                                        else f"${price}" if price 
                                        else "N/A"
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # Add delete buttons for each company
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
        # Check if there are companies in this sector
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

# About section in sidebar
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("""
This app allows you to track stock prices by sector.
1. Add sectors to organize your stocks
2. Add companies with their ticker codes
3. View current prices updated in real-time
""")