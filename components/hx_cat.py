import streamlit as st
import pandas as pd
from components.utils import get_today_return

def hx_cat():
    st.header("HX-CAT Companies")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        data = []
        for company in st.session_state.data["companies"]:
            if company.get("hx_cat", False):
                day_return, _ = get_today_return(company["ticker"])
                if day_return is not None:
                    data.append({
                        "Company": company["name"],
                        "Sector": company["sector"],
                        "Day Change (%)": day_return
                    })

        if not data:
            st.info("No companies tagged as HX-CAT found.")
        else:
            df = pd.DataFrame(data)
            df = df.sort_values(by="Day Change (%)", ascending=False)
            df = df.reset_index(drop=True)

            st.subheader("HX-CAT Companies Ranked by Daily Return")
            st.dataframe(df, use_container_width=True)