import streamlit as st
import datetime
import uuid
from components.utils import get_current_stock_price, save_data

def add_company_form():
    st.subheader("Add Company to Track" if not st.session_state.get("edit_mode", False) else "Edit Company")

    if not st.session_state.data["sectors"]:
        st.warning("Please add at least one sector first!")
        return

    # Initialize edit mode
    company = None
    if st.session_state.get("edit_mode", False) and st.session_state.get("edit_company"):
        company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.edit_company), None)
        if not company:
            st.error("Company not found for editing.")
            return

    # Set default values for form
    default_values = {
        "company_name": company["name"] if company else "",
        "ticker_code": company["ticker"].replace(".NS", "").replace(".BO", "") if company else "",
        "selected_sector": company["sector"] if company else st.session_state.data["sectors"][0],
        "buy_price": float(company["buy_price"]) if company else 0.00,
        "shares": int(company["shares"]) if company else 0,
        "purchase_date": datetime.datetime.strptime(company["purchase_date"], "%Y-%m-%d").date() if company else datetime.date.today(),
        "suffix": ".NS" if company and company["ticker"].endswith(".NS") else ".BO" if company and company["ticker"].endswith(".BO") else ".NS",
        "move_to_hx": "Yes" if company and company.get("hx_cat", False) else "No",
        "screener_link": company.get("screener_link", "") if company else "",
        "view_weblink": company.get("view_weblink", "") if company else ""
    }

    with st.form("add_company_form"):
        company_name = st.text_input("Company Name", value=default_values["company_name"], placeholder="e.g. Reliance Industries")
        ticker_code = st.text_input("Ticker Code", value=default_values["ticker_code"], placeholder="e.g. RELIANCE")
        selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"],
                                       index=st.session_state.data["sectors"].index(default_values["selected_sector"])
                                       if default_values["selected_sector"] in st.session_state.data["sectors"] else 0)
        buy_price = st.number_input("Buy Price", min_value=0.00, value=default_values["buy_price"], format="%.2f",
                                    placeholder="Enter your purchase price")
        shares = st.number_input("Number of Shares", min_value=0, value=default_values["shares"], step=1,
                                 placeholder="Enter number of shares bought")
        purchase_date = st.date_input("Purchase Date", value=default_values["purchase_date"],
                                      max_value=datetime.date.today())
        suffix_options = [".NS", ".BO"]
        suffix = st.selectbox("Exchange Suffix", suffix_options, index=suffix_options.index(default_values["suffix"]),
                              help=".NS for NSE, .BO for BSE")
        move_to_hx = st.selectbox("Move to HX Category", ["No", "Yes"], index=1 if default_values["move_to_hx"] == "Yes" else 0,
                                  help="Select Yes to tag as HX-CAT")
        screener_link = st.text_input("Screener Link", value=default_values["screener_link"], placeholder="e.g. https://www.screener.in/company/RELIANCE/")
        view_weblink = st.text_input("View Weblink", value=default_values["view_weblink"], placeholder="e.g. https://www.nseindia.com/companies/RELIANCE")

        col1, col2 = st.columns(2)
        with col1:
            submit_company = st.form_submit_button("Add Company" if not st.session_state.get("edit_mode", False) else "Update Company")
        with col2:
            cancel_button = st.form_submit_button("Cancel")

        if submit_company and company_name and ticker_code:
            full_ticker = f"{ticker_code}{suffix}"
            existing_tickers = [c["ticker"] for c in st.session_state.data["companies"] if not company or c["id"] != company["id"]]
            if full_ticker in existing_tickers:
                st.error(f"Company with ticker '{full_ticker}' already exists!")
            else:
                test_price = get_current_stock_price(full_ticker)
                if test_price is not None:
                    company_data = {
                        "id": company["id"] if company else str(uuid.uuid4()),
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
                        "grow_link": "",
                        "screener_link": screener_link,
                        "view_weblink": view_weblink,
                        "is_ipo": False
                    }
                    if company:  # Update existing company
                        st.session_state.data["companies"] = [company_data if c["id"] == company["id"] else c for c in st.session_state.data["companies"]]
                        # Update transaction if exists
                        existing_transaction = next((t for t in st.session_state.data["transactions"] if t["company_id"] == company["id"] and t["type"] == "buy"), None)
                        if existing_transaction and shares > 0 and buy_price > 0:
                            existing_transaction.update({
                                "amount": company_data["total_invested"],
                                "shares": company_data["shares"],
                                "price_per_share": company_data["buy_price"],
                                "date": company_data["purchase_date"],
                                "profit_loss": 0.0
                            })
                        elif shares > 0 and buy_price > 0 and not existing_transaction:
                            transaction = {
                                "company_id": company_data["id"],
                                "type": "buy",
                                "amount": company_data["total_invested"],
                                "shares": company_data["shares"],
                                "price_per_share": company_data["buy_price"],
                                "date": company_data["purchase_date"],
                                "profit_loss": 0.0
                            }
                            st.session_state.data["transactions"].append(transaction)
                        st.success(f"Company '{company_name}' updated successfully!")
                    else:  # Add new company
                        st.session_state.data["companies"].append(company_data)
                        if shares > 0 and buy_price > 0:
                            transaction = {
                                "company_id": company_data["id"],
                                "type": "buy",
                                "amount": company_data["total_invested"],
                                "shares": company_data["shares"],
                                "price_per_share": company_data["buy_price"],
                                "date": company_data["purchase_date"],
                                "profit_loss": 0.0
                            }
                            st.session_state.data["transactions"].append(transaction)
                        st.success(f"Company '{company_name}' added successfully!")
                    save_data(st.session_state.data)
                    # Reset session state
                    st.session_state.add_company_clicked = False
                    st.session_state.edit_company = None
                    st.session_state.edit_mode = False
                    st.rerun()
                else:
                    st.error(f"Could not fetch data for ticker '{full_ticker}'. Please verify the ticker code.")
        elif submit_company:
            st.error("Please fill Company Name and Ticker Code.")
        elif cancel_button:
            st.session_state.add_company_clicked = False
            st.session_state.edit_company = None
            st.session_state.edit_mode = False
            st.rerun()