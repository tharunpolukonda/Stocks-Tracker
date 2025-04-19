import streamlit as st
import datetime
import uuid
from components.utils import get_current_stock_price, save_data

def add_ipo_form():
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