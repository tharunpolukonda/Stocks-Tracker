import streamlit as st
import pandas as pd
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss

def portfolio_dashboard():
    st.header("Portfolio Dashboard")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        # Debug buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Debug: List Tickers"):
                st.write([c["ticker"] for c in st.session_state.data["companies"]])
        with col2:
            if st.button("Debug: Clear Cache"):
                st.session_state.return_cache = {}
                st.rerun()

        # Prepare data for all components
        component_data = []
        for company in st.session_state.data["companies"]:
            day_return, day_return_msg = get_today_return(company["ticker"])
            current_price = get_current_stock_price(company["ticker"])
            buy_price = company.get("buy_price", 0)
            shares = company.get("shares", 0)
            total_invested = company.get("total_invested", buy_price * shares)
            currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"

            pl_data = calculate_profit_loss(buy_price, shares, current_price) if current_price and shares > 0 else None

            company_data = {
                "Company": company["name"],
                "Sector": company["sector"],
                "Day Change (%)": day_return if day_return is not None else None,
                "Day Change Display": f"{day_return:.2f}%" if day_return is not None else f"N/A ({day_return_msg})",
                "P/L": pl_data["profit_loss"] if pl_data else 0,
                "P/L %": pl_data["profit_loss_percent"] if pl_data else 0,
                "Invested Amount": total_invested,
                "Shares": shares,
                "HX-CAT": company.get("hx_cat", False),
                "Formatted P/L": f"{currency_symbol}{pl_data['profit_loss']:.2f}" if pl_data else "N/A",
                "Formatted Invested": f"{currency_symbol}{total_invested:.2f}"
            }
            if day_return is None:
                print(f"Day Change N/A for {company['ticker']}: {day_return_msg}")
            component_data.append(company_data)

        df_all = pd.DataFrame(component_data)

        # Component 1: Top 5 Companies by High Day Change (Holding)
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 5 Companies by High Day Change (Holding)")
            df_filtered = df_all[df_all["Shares"] > 0]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "Formatted P/L", "P/L %", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data and holdings.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 2: Top 5 Companies by High P/L% (Holding)
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 5 Companies by High P/L% (Holding)")
            df_filtered = df_all[df_all["Shares"] > 0]
            if not df_filtered.empty and df_filtered["P/L %"].notna().any():
                df_sorted = df_filtered.sort_values(by="P/L %", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid P/L data and holdings.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 3: Top 5 HX-Category Companies by High Day Change
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 5 HX-Category Companies by High Day Change")
            df_filtered = df_all[df_all["HX-CAT"] == True]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=False).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No HX-Category companies with valid day change data.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 4: Top 5 HX-Category Companies by Low Day Change
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 5 HX-Category Companies by Low Day Change")
            df_filtered = df_all[df_all["HX-CAT"] == True]
            if not df_filtered.empty and df_filtered["Day Change (%)"].notna().any():
                df_sorted = df_filtered.sort_values(by="Day Change (%)", ascending=True).head(5)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No HX-Category companies with valid day change data.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 5: Top 10 Companies by High Day Change (All)
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 10 Companies by High Day Change (All)")
            if not df_all.empty and df_all["Day Change (%)"].notna().any():
                df_sorted = df_all.sort_values(by="Day Change (%)", ascending=False).head(10)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 6: Top 10 Companies by Low Day Change (All)
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Top 10 Companies by Low Day Change (All)")
            if not df_all.empty and df_all["Day Change (%)"].notna().any():
                df_sorted = df_all.sort_values(by="Day Change (%)", ascending=True).head(10)
                st.dataframe(
                    df_sorted[["Company", "Sector", "Day Change Display", "P/L %", "Formatted P/L", "Formatted Invested"]],
                    use_container_width=True,
                    column_config={
                        "Company": st.column_config.TextColumn(label="Company"),
                        "Sector": st.column_config.TextColumn(label="Sector"),
                        "Day Change Display": st.column_config.TextColumn(label="Day Change"),
                        "P/L %": st.column_config.NumberColumn(label="P/L %", format="%.2f"),
                        "Formatted P/L": st.column_config.TextColumn(label="P/L"),
                        "Formatted Invested": st.column_config.TextColumn(label="Invested Amount")
                    }
                )
            else:
                st.info("No companies with valid day change data.")
            st.markdown('</div>', unsafe_allow_html=True)