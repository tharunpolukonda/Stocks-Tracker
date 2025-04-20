import streamlit as st
import pandas as pd
import datetime
from components.utils import get_current_stock_price

def track_ipo():
    st.subheader("Track IPOs")

    # Filter companies with listing_price > 0 (IPO companies only)
    ipo_companies = [company for company in st.session_state.data["companies"] if company.get("listing_price", 0) > 0]

    if not ipo_companies:
        st.warning("No IPOs added yet. Please add an IPO first.")
        return

    # Prepare data for the table
    table_data = []
    for company in ipo_companies:
        current_price = get_current_stock_price(company["ticker"]) or 0.0
        listing_price = company.get("listing_price", 0.0)
        issue_price = company.get("issue_price", 0.0)
        buy_price = company.get("buy_price", 0.0)
        shares = company.get("shares", 0)
        listed_date_str = company.get("listed_date", "")

        # Calculate P/L% to Listing Price
        pl_listing = ((current_price - listing_price) / listing_price * 100) if listing_price > 0 else 0.0
        pl_listing = round(pl_listing, 2)

        # Calculate P/L% to Issue Price
        pl_issue = ((current_price - issue_price) / issue_price * 100) if issue_price > 0 else 0.0
        pl_issue = round(pl_issue, 2)

        # Calculate P/L% (to Buy Price)
        pl_buy = "N/A" if shares == 0 or buy_price == 0 else round(((current_price - buy_price) / buy_price * 100), 2)

        # Calculate 3MLIP and 6MLIP
        try:
            listed_date = datetime.datetime.strptime(listed_date_str, "%Y-%m-%d").date()
            three_month_lip = (listed_date + datetime.timedelta(days=90)).strftime("%d-%m-%Y")
            six_month_lip = (listed_date + datetime.timedelta(days=180)).strftime("%d-%m-%Y")
        except ValueError:
            three_month_lip = "N/A"
            six_month_lip = "N/A"

        table_data.append({
            "Company Name": company["name"],
            "Sector Name": company["sector"],
            "Current Price": f"₹{current_price:.2f}",
            "P/L% to Listing Price": f"{pl_listing:.2f}%" if pl_listing != 0.0 else "N/A",
            "P/L% to Issue Price": f"{pl_issue:.2f}%" if pl_issue != 0.0 else "N/A",
            "P/L%": f"{pl_buy}%" if pl_buy != "N/A" else "N/A",
            "3MLIP": three_month_lip,
            "6MLIP": six_month_lip
        })

    # Display table
    df = pd.DataFrame(table_data)
    st.markdown('<div class="track-ipo-table">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)