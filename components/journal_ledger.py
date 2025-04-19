import streamlit as st
import pandas as pd
import datetime
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss, save_data

def journal_ledger():
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