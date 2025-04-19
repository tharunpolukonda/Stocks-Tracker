import streamlit as st
import pandas as pd
from components.utils import get_today_return

def high_return():
    st.header("High Return Stocks")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
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