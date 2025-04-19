import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.utils import get_current_stock_price, calculate_profit_loss, get_indian_market_cap_category

def visualize_companies():
    st.header("Company Investment Analysis")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        sectors = ["All Sectors"] + st.session_state.data["sectors"]
        sector_key = "visualize_sector_filter"

        selected_sector = st.selectbox(
            "Filter by Sector",
            sectors,
            index=sectors.index(st.session_state.visualize_sector),
            key=sector_key
        )

        if selected_sector != st.session_state.visualize_sector:
            st.session_state.visualize_sector = selected_sector
            st.session_state.filter_cap_wise = False
            st.session_state.filter_combined_caps = False

        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("Filter Cap Wise", key="filter_cap_wise_button",
                         type="primary" if st.session_state.filter_cap_wise else "secondary"):
                st.session_state.filter_cap_wise = not st.session_state.filter_cap_wise
                st.session_state.filter_combined_caps = False
                if st.session_state.filter_cap_wise:
                    st.session_state.selected_cap = "Large-Cap"
        with col3:
            if st.button("Filter Combined Caps", key="filter_combined_caps_button",
                         type="primary" if st.session_state.filter_combined_caps else "secondary"):
                st.session_state.filter_combined_caps = not st.session_state.filter_combined_caps
                st.session_state.filter_cap_wise = False

        # Sector-based Visualization
        if not st.session_state.filter_cap_wise and not st.session_state.filter_combined_caps:
            data = []
            total_invested = 0
            total_pl = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])

                    pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None

                    if total_invested_company > 0:
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        if pl_data:
                            total_pl += pl_data["profit_loss"]
                        data.append(company_data)

            if not data:
                st.info(f"No invested companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")

                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

                # Display combined P/L
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    pl_label = "Profit" if total_pl >= 0 else "Loss"
                    st.metric(f"Combined {pl_label} for {selected_sector}",
                              f"{currency_symbol}{abs(total_pl):.2f}")

        # Cap-wise Visualization
        elif st.session_state.filter_cap_wise:
            cap_categories = ["Large-Cap", "Mid-Cap", "Small-Cap", "Micro-Cap"]
            selected_cap = st.selectbox(
                "Select Market Cap Category",
                cap_categories,
                index=cap_categories.index(st.session_state.selected_cap),
                key="cap_filter"
            )

            if selected_cap != st.session_state.selected_cap:
                st.session_state.selected_cap = selected_cap

            data = []
            total_invested = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])

                    cap_category, _ = get_indian_market_cap_category(company["ticker"])

                    if cap_category == selected_cap and total_invested_company > 0:
                        pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        data.append(company_data)

            if not data:
                st.info(f"No {selected_cap} companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")

                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"{selected_cap} Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

        # Combined Caps Visualization
        elif st.session_state.filter_combined_caps:
            data = []
            total_invested = 0
            for company in st.session_state.data["companies"]:
                if selected_sector == "All Sectors" or company["sector"] == selected_sector:
                    total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
                    shares = company.get("shares", 0)
                    current_price = get_current_stock_price(company["ticker"])

                    if total_invested_company > 0:
                        pl_data = calculate_profit_loss(total_invested_company / shares if shares > 0 else 0, shares, current_price) if current_price and shares > 0 else None
                        total_invested += total_invested_company
                        currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                        company_data = {
                            "Company": company["name"],
                            "Sector": company["sector"],
                            "Invested": total_invested_company,
                            "P/L": pl_data["profit_loss"] if pl_data else 0
                        }
                        data.append(company_data)

            if not data:
                st.info(f"No invested companies found for {selected_sector}.")
            else:
                df = pd.DataFrame(data)
                df["Weightage (%)"] = (df["Invested"] / total_invested * 100).round(2)
                df["P/L (Currency)"] = df["P/L"].apply(lambda x: f"{currency_symbol}{x:.2f}")

                # Create pie chart
                labels = [f"{row['Company']}\nP/L: {row['P/L (Currency)']}" for _, row in df.iterrows()]
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=df["Invested"],
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=[f"rgba(59, 130, 246, {0.6 + i*0.1})" for i in range(len(df))]),
                        textposition="inside"
                    )
                ])
                fig.update_layout(
                    title=f"All Companies Investment Weightage in {selected_sector}",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF",
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)