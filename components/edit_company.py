import streamlit as st
import datetime
from components.utils import get_current_stock_price, save_data

def edit_company_form():
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