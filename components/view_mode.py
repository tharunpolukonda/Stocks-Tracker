import streamlit as st
import pandas as pd
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss, save_data

def toggle_edit_company(company_id):
    st.session_state.edit_company = company_id if st.session_state.edit_company != company_id else None

def view_mode():
    st.header("View Mode - Portfolio by Sector")

    if not st.session_state.data["sectors"]:
        st.info("No sectors added yet. Click 'Add Sector' to get started.")
    elif not st.session_state.data["companies"]:
        st.info("No companies added yet. Click 'Add Company' or 'Add IPOs' to start tracking stocks.")
    else:
        # Check if viewing company details
        if "view_company_details" in st.session_state and st.session_state.view_company_details:
            company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.view_company_details), None)
            if company:
                st.markdown('<div class="company-details-container">', unsafe_allow_html=True)
                st.subheader(f"Details for {company['name']}")
                is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))
                current_price = get_current_stock_price(company["ticker"])
                day_return, day_return_msg = get_today_return(company["ticker"])
                buy_price = company.get("buy_price", 0)
                shares = company.get("shares", 0)
                total_invested = company.get("total_invested", buy_price * shares)
                currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                ticker_suffix = "NS" if company["ticker"].endswith(".NS") else "BO" if company["ticker"].endswith(".BO") else "Other"

                pl_data = None
                if current_price and shares > 0:
                    pl_data = calculate_profit_loss(buy_price, shares, current_price)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Company Name**: {company['name']}")
                    st.markdown(f"**Sector**: {company['sector']}")
                    st.markdown(f"**Ticker Code**: {company['ticker']}")
                    st.markdown(f"**Ticker Suffix**: {ticker_suffix}")
                    st.markdown(f"**Number of Shares**: {shares}")
                    st.markdown(f"**Each Share Price (Buy)**: {currency_symbol}{buy_price:.2f}")
                with col2:
                    st.markdown(f"**Day Change**: {day_return}% {'(N/A: ' + day_return_msg + ')' if day_return is None else ''}")
                    st.markdown(f"**Current Value**: {currency_symbol}{pl_data['current_value']:.2f} {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**P/L**: {currency_symbol}{pl_data['profit_loss']:.2f} {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**P/L %**: {pl_data['profit_loss_percent']:.2f}% {'(N/A)' if not pl_data else ''}")
                    st.markdown(f"**Type**: {'IPO' if is_ipo else 'Regular'}")

                if is_ipo:
                    st.markdown('<div class="ipo-details-container">', unsafe_allow_html=True)
                    st.subheader("IPO Details")
                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown(f"**Listing Price**: {currency_symbol}{company.get('listing_price', 0):.2f}")
                        st.markdown(f"**Issue Price**: {currency_symbol}{company.get('issue_price', 0):.2f}")
                    with col4:
                        st.markdown(f"**Issue Size**: {company.get('issue_size', 0)}")
                        st.markdown(f"**Listed Date**: {company.get('listed_date', 'N/A')}")
                        if company.get("grow_link"):
                            st.markdown(f"**Grow Link**: [{company['grow_link']}]({company['grow_link']})")
                    st.markdown('</div>', unsafe_allow_html=True)

                if st.button("Back to Sector"):
                    st.session_state.view_company_details = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # Sector selection or table view
        elif st.session_state.selected_sector_for_view is None:
            st.subheader("Select a Sector to View")

            cols = st.columns(3)

            for i, sector in enumerate(st.session_state.data["sectors"]):
                sector_companies = [c for c in st.session_state.data["companies"] if c["sector"] == sector]

                with cols[i % 3]:
                    st.markdown(f"### {sector}")
                    st.markdown(f"**Companies:** {len(sector_companies)}")

                    if sector_companies:
                        sector_invested = sum(c.get("total_invested", c.get("buy_price", 0) * c.get("shares", 0)) for c in sector_companies)
                        st.markdown(f"**Invested:** ₹{sector_invested:.2f}")

                    if st.button(f"View {sector}", key=f"view_{sector}"):
                        st.session_state.selected_sector_for_view = sector
                        st.rerun()

        else:
            selected_sector = st.session_state.selected_sector_for_view
            sector_companies = [c for c in st.session_state.data["companies"] if c["sector"] == selected_sector]

            if st.button("← Back to Sectors"):
                st.session_state.selected_sector_for_view = None
                st.rerun()

            st.subheader(f"{selected_sector} Sector Analysis")

            if not sector_companies:
                st.info(f"No companies added to the {selected_sector} sector yet.")
            else:
                sector_invested = sum(c.get("total_invested", c.get("buy_price", 0) * c.get("shares", 0)) for c in sector_companies)
                sector_current_value = 0
                sector_pl = 0

                # Sector metrics
                st.markdown('<div class="sector-metrics-container">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Invested", f"₹{sector_invested:.2f}")
                with col2:
                    st.metric("Current Value", f"₹{sector_current_value:.2f}")
                with col3:
                    st.metric("Profit/Loss", f"₹{sector_pl:.2f}")
                with col4:
                    st.metric("Companies", len(sector_companies))
                st.markdown('</div>', unsafe_allow_html=True)

                data = []
                for company in sector_companies:
                    current_price = get_current_stock_price(company["ticker"])
                    day_return, day_return_msg = get_today_return(company["ticker"])

                    buy_price = company.get("buy_price", 0)
                    shares = company.get("shares", 0)
                    total_invested = company.get("total_invested", buy_price * shares)
                    purchase_date = company.get("purchase_date", "N/A")
                    is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))

                    pl_data = None
                    if current_price and shares > 0:
                        pl_data = calculate_profit_loss(total_invested / shares if shares > 0 else 0, shares, current_price)
                        sector_current_value += pl_data["current_value"] if pl_data else 0
                        sector_pl += pl_data["profit_loss"] if pl_data else 0

                    currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"
                    ticker_suffix = "NS" if company["ticker"].endswith(".NS") else "BO" if company["ticker"].endswith(".BO") else "Other"

                    company_data = {
                        "Company": company["name"],
                        "Ticker": company["ticker"],
                        "Type": "IPO" if is_ipo else "Regular",
                        "Purchase Date": purchase_date,
                        "Current Price": f"{currency_symbol}{current_price:.2f}" if current_price else "N/A",
                        "Buy Price": f"{currency_symbol}{buy_price:.2f}",
                        "Shares": shares,
                        "Day Change": f"{day_return}%" if day_return is not None else f"N/A ({day_return_msg})",
                        "Invested": f"{currency_symbol}{total_invested:.2f}",
                        "Ticker Suffix": ticker_suffix,
                        "ID": company["id"],
                        "Actions": ""
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

                    data.append(company_data)

                # Update sector metrics
                st.markdown('<div class="sector-metrics-container">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Invested", f"₹{sector_invested:.2f}")
                with col2:
                    st.metric("Current Value", f"₹{sector_current_value:.2f}")
                with col3:
                    pl_label = "Profit" if sector_pl >= 0 else "Loss"
                    sector_pl_pct = (sector_pl / sector_invested * 100) if sector_invested > 0 else 0
                    st.metric(pl_label, f"₹{abs(sector_pl):.2f}", f"{sector_pl_pct:.2f}%",
                              delta_color="normal" if sector_pl >= 0 else "inverse")
                with col4:
                    st.metric("Companies", len(sector_companies))
                st.markdown('</div>', unsafe_allow_html=True)

                # Companies table
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                st.subheader("Companies in Sector")
                # Header row
                st.markdown('<div class="table-row">', unsafe_allow_html=True)
                cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
                headers = ["Company", "Ticker", "Type", "Purchase Date", "Current Price", "Buy Price",
                           "Shares", "Day Change", "Current Value", "P/L", "Actions"]
                for col, header in zip(cols, headers):
                    with col:
                        st.markdown(f'<div class="table-cell"><b>{header}</b></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Data rows
                for company_data in data:
                    is_ipo = company_data["Type"] == "IPO"
                    st.markdown('<div class="table-row">', unsafe_allow_html=True)
                    cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
                    with cols[0]:
                        st.markdown(
                            f'<div class="table-cell"><span style="color: {"#00FF00" if is_ipo else "#1E3A8A"}; font-weight: {"bold" if is_ipo else "normal"};">{company_data["Company"]}</span></div>',
                            unsafe_allow_html=True
                        )
                    with cols[1]:
                        st.markdown(f'<div class="table-cell">{company_data["Ticker"]}</div>', unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown(f'<div class="table-cell">{company_data["Type"]}</div>', unsafe_allow_html=True)
                    with cols[3]:
                        st.markdown(f'<div class="table-cell">{company_data["Purchase Date"]}</div>', unsafe_allow_html=True)
                    with cols[4]:
                        st.markdown(f'<div class="table-cell">{company_data["Current Price"]}</div>', unsafe_allow_html=True)
                    with cols[5]:
                        st.markdown(f'<div class="table-cell">{company_data["Buy Price"]}</div>', unsafe_allow_html=True)
                    with cols[6]:
                        st.markdown(f'<div class="table-cell">{company_data["Shares"]}</div>', unsafe_allow_html=True)
                    with cols[7]:
                        st.markdown(f'<div class="table-cell">{company_data["Day Change"]}</div>', unsafe_allow_html=True)
                    with cols[8]:
                        st.markdown(f'<div class="table-cell">{company_data["Current Value"]}</div>', unsafe_allow_html=True)
                    with cols[9]:
                        st.markdown(f'<div class="table-cell">{company_data["P/L"]}</div>', unsafe_allow_html=True)
                    with cols[10]:
                        st.markdown('<div class="table-cell">', unsafe_allow_html=True)
                        col_edit, col_remove, col_view = st.columns(3)
                        with col_edit:
                            if st.button("Edit", key=f"edit_{company_data['ID']}"):
                                toggle_edit_company(company_data["ID"])
                                st.rerun()
                        with col_remove:
                            if st.button("Remove", key=f"remove_{company_data['ID']}"):
                                st.session_state.data["companies"] = [
                                    c for c in st.session_state.data["companies"] if c["id"] != company_data["ID"]
                                ]
                                st.session_state.data["transactions"] = [
                                    t for t in st.session_state.data["transactions"] if t["company_id"] != company_data["ID"]
                                ]
                                save_data(st.session_state.data)
                                st.success(f"Company '{company_data['Company']}' removed successfully!")
                                st.rerun()
                        with col_view:
                            if st.button("View", key=f"view_details_{company_data['ID']}"):
                                st.session_state.view_company_details = company_data["ID"]
                                st.session_state.selected_sector_for_view = None
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)