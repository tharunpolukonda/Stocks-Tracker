import streamlit as st
import pandas as pd
from components.utils import get_today_return

def invest_companies():
    st.header("Invested Companies")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
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