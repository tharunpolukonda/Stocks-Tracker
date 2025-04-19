import streamlit as st
import yfinance as yf
import json
import pandas as pd
from github import Github
from datetime import datetime, timedelta
import os
import numpy as np

def load_data():
    """Load stock data from GitHub repository."""
    try:
        github_token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]
        file_path = "stock_data.json"

        g = Github(github_token)
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents(file_path)
        data = json.loads(file_content.decoded_content.decode('utf-8'))
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {"sectors": [], "companies": [], "transactions": []}

def save_data(data):
    """Save stock data to GitHub repository."""
    try:
        github_token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]
        file_path = "stock_data.json"

        g = Github(github_token)
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents(file_path)
        
        # Update the file
        repo.update_file(
            path=file_path,
            message="Update stock_data.json",
            content=json.dumps(data, indent=2),
            sha=file_content.sha
        )
    except Exception as e:
        st.error(f"Error saving data: {e}")

def get_current_stock_price(ticker):
    """Fetch current stock price using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return round(float(price), 2) if not pd.isna(price) else None
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None

def get_today_return(ticker):
    """Calculate today's return percentage."""
    if "return_cache" not in st.session_state:
        st.session_state.return_cache = {}

    cache_key = f"{ticker}_return_{datetime.now().date()}"
    if cache_key in st.session_state.return_cache:
        return st.session_state.return_cache[cache_key]

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="2d")
        if len(history) < 2:
            st.session_state.return_cache[cache_key] = (None, "Insufficient data")
            return None, "Insufficient data"

        today_close = history["Close"].iloc[-1]
        yesterday_close = history["Close"].iloc[-2]

        if pd.isna(today_close) or pd.isna(yesterday_close):
            st.session_state.return_cache[cache_key] = (None, "Price data unavailable")
            return None, "Price data unavailable"

        day_return = ((today_close - yesterday_close) / yesterday_close) * 100
        st.session_state.return_cache[cache_key] = (round(float(day_return), 2), "")
        return round(float(day_return), 2), ""
    except Exception as e:
        st.session_state.return_cache[cache_key] = (None, str(e))
        return None, str(e)

def calculate_profit_loss(buy_price, shares, current_price):
    """Calculate profit/loss and related metrics."""
    if shares <= 0 or current_price is None:
        return None

    current_value = current_price * shares
    invested_value = buy_price * shares
    profit_loss = current_value - invested_value
    profit_loss_percent = (profit_loss / invested_value) * 100 if invested_value > 0 else 0

    return {
        "current_value": round(current_value, 2),
        "profit_loss": round(profit_loss, 2),
        "profit_loss_percent": round(profit_loss_percent, 2)
    }

def get_indian_market_cap_category(ticker):
    """Determine market cap category for Indian stocks."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        market_cap = info.get("marketCap")

        if market_cap is None:
            return "Unknown", 0

        # Convert to INR crores (1 crore = 10 million)
        market_cap_crores = market_cap / 1_00_00_000

        # Indian market cap categories
        if market_cap_crores > 20000:
            return "Large-Cap", market_cap_crores
        elif 5000 <= market_cap_crores <= 20000:
            return "Mid-Cap", market_cap_crores
        elif 250 <= market_cap_crores < 5000:
            return "Small-Cap", market_cap_crores
        else:
            return "Micro-Cap", market_cap_crores
    except Exception as e:
        print(f"Error fetching market cap for {ticker}: {e}")
        return "Unknown", 0