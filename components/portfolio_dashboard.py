import streamlit as st
import pandas as pd
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss

def portfolio_dashboard():
    st.header("Portfolio Dashboard")

    if not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        # Portfolio Summary
        total_invested = 0
        total_current_value = 0
        
        for company in st.session_state.data["companies"]:
            total_invested_company = company.get("total_invested", company.get("buy_price", 0) * company.get("shares", 0))
            shares = company.get("shares", 0)
            current_price = get_current_stock_price(company["ticker"])
            
            if total_invested_company > 0 and shares > 0 and current_price:
                total_invested += total_invested_company
                current_val = current_price * shares
                total_current_value += current_val
        
        total_profit_loss = total_current_value - total_invested
        total_profit_loss_percent = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        st.subheader("Portfolio Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Invested", f"₹{total_invested:.2f}")
        with col2:
            st.metric("Current Value", f"₹{total_current_value:.2f}")
        with col3:
            pl_label = "Profit" if total_profit_loss >= 0 else "Loss"
            st.metric(pl_label, f"₹{abs(total_profit_loss):.2f}", 
                     f"{total_profit_loss_percent:.2f}%", 
                     delta_color="normal" if total_profit_loss >= 0 else "inverse")
        with col4:
            st.metric("Holdings", f"{len(st.session_state.data['companies'])} Stocks")
        
        st.markdown("---")

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
                "Formatted Invested": f"{currency_symbol}{total_invested:.2f}",
                "Is IPO": company.get("is_ipo", False),
                "Screener Link": company.get("screener_link", ""),
                "View Weblink": company.get("view_weblink", "")
            }
            if day_return is None:
                print(f"Day Change N/A for {company['ticker']}: {day_return_msg}")
            component_data.append(company_data)

        df_all = pd.DataFrame(component_data)
        
        # Component 1: Companies by Sector
        with st.container():
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.subheader("Companies by Sector")
            if not st.session_state.data["sectors"]:
                st.info("No sectors available. Please add a sector first.")
            else:
                selected_sector = st.selectbox("Select Sector", st.session_state.data["sectors"], key="sector_select")
                only_ipo = st.checkbox("Only IPO", key="only_ipo_checkbox")
                
                df_sector = df_all[df_all["Sector"] == selected_sector]
                if only_ipo:
                    df_sector = df_sector[df_sector["Is IPO"] == True]
                
                if not df_sector.empty and df_sector["Day Change (%)"].notna().any():
                    df_sorted = df_sector.sort_values(by="Day Change (%)", ascending=False)
                    
                    # Render custom table with HTML for styling IPO names and clickable links
                    st.markdown('<div class="table-row">', unsafe_allow_html=True)
                    cols = st.columns([2, 1, 1, 1, 2, 2])
                    headers = ["Company Name", "Day Change", "P/L", "P/L %", "View Weblink", "Screener Link"]
                    for col, header in zip(cols, headers):
                        with col:
                            st.markdown(f'<div class="table-cell"><b>{header}</b></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    for _, row in df_sorted.iterrows():
                        is_ipo = row["Is IPO"]
                        company_name = row["Company"]
                        display_name = f'<span style="color: #00FF00; font-weight: bold;">{company_name}</span>' if is_ipo else company_name
                        screener_link = row["Screener Link"]
                        view_weblink = row["View Weblink"]
                        screener_display = f'<a href="{screener_link}" target="_blank">Click here</a>' if screener_link else "N/A"
                        weblink_display = f'<a href="{view_weblink}" target="_blank">Click here</a>' if view_weblink else "N/A"
                        
                        st.markdown('<div class="table-row">', unsafe_allow_html=True)
                        cols = st.columns([2, 1, 1, 1, 2, 2])
                        with cols[0]:
                            st.markdown(f'<div class="table-cell">{display_name}</div>', unsafe_allow_html=True)
                        with cols[1]:
                            st.markdown(f'<div class="table-cell">{row["Day Change Display"]}</div>', unsafe_allow_html=True)
                        with cols[2]:
                            st.markdown(f'<div class="table-cell">{row["Formatted P/L"]}</div>', unsafe_allow_html=True)
                        with cols[3]:
                            st.markdown(f'<div class="table-cell">{row["P/L %"]:.2f}%</div>', unsafe_allow_html=True)
                        with cols[4]:
                            st.markdown(f'<div class="table-cell">{weblink_display}</div>', unsafe_allow_html=True)
                        with cols[5]:
                            st.markdown(f'<div class="table-cell">{screener_display}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info(f"No {'IPO ' if only_ipo else ''}companies found in the {selected_sector} sector with valid data.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Component 2: Top 5 Companies by High Day Change (Holding)
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

        # Component 3: Top 5 Companies by High P/L% (Holding)
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

        # Component 4: Top 5 HX-Category Companies by High Day Change
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

        # Component 5: Top 5 HX-Category Companies by Low Day Change
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

        # Component 6: Top 10 Companies by High Day Change (All)
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

        # Component 7: Top 10 Companies by Low Day Change (All)
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