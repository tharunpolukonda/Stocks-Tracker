import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss

def search_view():
    """Display company search results, details, and components (e.g., line chart) triggered by specific buttons."""
    st.header("Search Companies")

    # Get search query from session state
    search_query = st.session_state.search_query.lower().strip()

    if not search_query:
        st.info("Please enter a search query to find companies.")
        return

    # Filter companies by search query
    matching_companies = [
        company for company in st.session_state.data["companies"]
        if search_query in company["name"].lower()
    ]

    if not matching_companies:
        st.warning(f"No companies found matching '{search_query}'.")
        return

    # Check if viewing company details
    if st.session_state.view_company_details:
        company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.view_company_details), None)
        if company:
            st.markdown('<div class="company-details-container">', unsafe_allow_html=True)
            st.subheader(f"Details for {company['name']}")
            is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))
            current_price = get_current_stock_price(company["ticker"])
            day_return, day_return_msg = get_today_return(company["ticker"])
            buy_price = company.get("buy_price", 0.0)
            shares = company.get("shares", 0)
            total_invested = company.get("total_invested", buy_price * shares)
            currency_symbol = "₹" if company["ticker"].endswith(('.NS', '.BO')) else "$"

            # Calculate P/L data
            pl_data = None
            if current_price and shares > 0:
                pl_data = calculate_profit_loss(buy_price, shares, current_price)
            current_price_display = f"{currency_symbol}{current_price:.2f}" if current_price else "N/A"
            day_change_display = f"{day_return:.2f}%" if day_return is not None else f"N/A ({day_return_msg})"
            pl_value = pl_data["profit_loss"] if pl_data and shares > 0 else 0.0
            pl_percent = pl_data["profit_loss_percent"] if pl_data and shares > 0 and buy_price > 0 else "N/A"
            pl_display = f"{currency_symbol}{pl_value:.2f}" if shares > 0 else "N/A"
            pl_percent_display = f"{pl_percent:.2f}%" if pl_percent != "N/A" else "N/A"

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Company Name**: {company['name']}")
                st.markdown(f"**Sector**: {company['sector']}")
                st.markdown(f"**Ticker**: {company['ticker']}")
                st.markdown(f"**Type**: {'IPO' if is_ipo else 'Regular'}")
                st.markdown(f"**Purchase Date**: {company.get('purchase_date', 'N/A')}")
                st.markdown(f"**Buy Price**: {currency_symbol}{buy_price:.2f}")
                st.markdown(f"**Shares**: {shares}")
                st.markdown(f"**Total Invested**: {currency_symbol}{total_invested:.2f}")
            with col2:
                st.markdown(f"**Current Price**: {current_price_display}")
                st.markdown(f"**Day Change**: {day_change_display}")
                st.markdown(f"**P/L**: {pl_display}")
                st.markdown(f"**P/L %**: {pl_percent_display}")
                screener_link = company.get('screener_link', '')
                view_weblink = company.get('view_weblink', '')
                st.markdown(f"**Screener Link**: [{'Click here'}]({screener_link})" if screener_link else "**Screener Link**: N/A", unsafe_allow_html=True)
                st.markdown(f"**View Weblink**: [{'Click here'}]({view_weblink})" if view_weblink else "**View Weblink**: N/A", unsafe_allow_html=True)

            if is_ipo:
                st.markdown('<div class="ipo-details-container">', unsafe_allow_html=True)
                st.subheader("IPO Details")
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f"**Listing Price**: {currency_symbol}{company.get('listing_price', 0):.2f}")
                    st.markdown(f"**Issue Price**: {currency_symbol}{company.get('issue_price', 0):.2f}")
                    pl_listing = ((current_price - company.get('listing_price', 0)) / company.get('listing_price', 0) * 100) if current_price and company.get('listing_price', 0) > 0 else 0.0
                    st.markdown(f"**P/L % to Listing Price**: {pl_listing:.2f}%")
                    st.markdown(f"**Subscription Rate**: {company.get('subscription_rate', 0)}x")
                with col4:
                    st.markdown(f"**Issue Size**: {company.get('issue_size', 0)}")
                    st.markdown(f"**Listed Date**: {company.get('listed_date', 'N/A')}")
                    st.markdown(f"**Grow Link**: [{'Click here'}]({company['grow_link']})" if company.get("grow_link") else "**Grow Link**: N/A", unsafe_allow_html=True)
                    pl_issue = ((current_price - company.get('issue_price', 0)) / company.get('issue_price', 0) * 100) if current_price and company.get('issue_price', 0) > 0 else 0.0
                    st.markdown(f"**P/L % to Issue Price**: {pl_issue:.2f}%")

                # Calculate 3MLP and 6MLP
                listed_date_str = company.get('listed_date', '')
                if listed_date_str and listed_date_str != 'N/A':
                    try:
                        listed_date = datetime.strptime(listed_date_str, "%Y-%m-%d").date()
                        three_month_lip = (listed_date + timedelta(days=90)).strftime("%d-%m-%Y")
                        six_month_lip = (listed_date + timedelta(days=180)).strftime("%d-%m-%Y")
                        st.markdown(f"**3-Month Lock-in Period (3MLP)**: {three_month_lip}")
                        st.markdown(f"**6-Month Lock-in Period (6MLP)**: {six_month_lip}")
                    except ValueError:
                        st.markdown(f"**3-Month Lock-in Period (3MLP)**: N/A")
                        st.markdown(f"**6-Month Lock-in Period (6MLP)**: N/A")
                else:
                    st.markdown(f"**3-Month Lock-in Period (3MLP)**: N/A")
                    st.markdown(f"**6-Month Lock-in Period (6MLP)**: N/A")

                st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Back to Search Results"):
                st.session_state.view_company_details = None
                st.session_state.active_component = None  # Reset when going back
                st.rerun()

            # Initialize active_component if not set
            if "active_component" not in st.session_state:
                st.session_state.active_component = None

            # Buttons to toggle components
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Graphical View", key=f"graphical_view_{company['ticker']}"):
                    st.session_state.active_component = "graphical_view"
                    st.rerun()
            with col2:
                if st.button("Financial Metrics", key=f"financial_metrics_{company['ticker']}"):
                    st.session_state.active_component = "financial_metrics"
                    st.rerun()

            # Display components based on active_component
            if st.session_state.active_component:
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                
                # Graphical View: Line chart component
                if st.session_state.active_component == "graphical_view":
                    st.subheader(f"Stock Price History for {company['name']} (Daily)")
                    
                    # Time period filter
                    time_period = st.selectbox(
                        "Select Time Period",
                        options=["1 Year", "3 Years", "5 Years"],
                        index=0,  # Default to 1 Year
                        key=f"time_period_{company['ticker']}"
                    )
                    
                    try:
                        # Fetch stock data
                        ticker = company["ticker"]
                        stock = yf.Ticker(ticker)
                        end_date = datetime.now()
                        listed_date_str = company.get('listed_date', '')
                        
                        # Map time period to days and yfinance period
                        period_map = {
                            "1 Year": {"days": 365, "period": "1y"},
                            "3 Years": {"days": 3 * 365, "period": "3y"},
                            "5 Years": {"days": 5 * 365, "period": "5y"}
                        }
                        selected_days = period_map[time_period]["days"]
                        yf_period = period_map[time_period]["period"]
                        
                        # Determine start date: use listing date if available and within selected period
                        if listed_date_str and listed_date_str != 'N/A':
                            try:
                                listed_date = datetime.strptime(listed_date_str, "%Y-%m-%d")
                                days_since_listing = (end_date - listed_date).days
                                if days_since_listing < selected_days:
                                    start_date = listed_date
                                else:
                                    start_date = end_date - timedelta(days=selected_days)
                            except ValueError:
                                start_date = end_date - timedelta(days=selected_days)
                        else:
                            start_date = end_date - timedelta(days=selected_days)
                        
                        # Fetch daily stock data
                        data = stock.history(start=start_date, end=end_date, interval="1d")
                        
                        if data.empty:
                            st.warning(f"No stock price data available for {ticker}. The company may not have sufficient historical data.")
                        else:
                            # Determine price column: prefer 'Adj Close', fallback to 'Close'
                            price_column = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
                            if price_column not in data.columns:
                                st.error(f"No valid price data ('Adj Close' or 'Close') available for {ticker}.")
                            else:
                                # Create line chart
                                fig = go.Figure()
                                fig.add_trace(
                                    go.Scatter(
                                        x=data.index,
                                        y=data[price_column],
                                        mode='lines',
                                        name=price_column,
                                        line=dict(color='#1e90ff', width=2)
                                    )
                                )
                                
                                # Customize layout
                                chart_title = f"{ticker} Stock Price (since {start_date.strftime('%Y-%m-%d')})" if start_date > end_date - timedelta(days=selected_days) else f"{ticker} {time_period} Stock Price"
                                fig.update_layout(
                                    title={
                                        'text': chart_title,
                                        'y': 0.9,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top',
                                        'font': dict(family='Georgia', size=20, color='#f0f4f8')
                                    },
                                    xaxis=dict(
                                        title='Date',
                                        titlefont=dict(family='Lato', size=14, color='#f0f4f8'),
                                        tickfont=dict(family='Lato', size=12, color='#f0f4f8'),
                                        gridcolor='rgba(240, 244, 248, 0.2)',
                                        tickformat='%Y-%m-%d',
                                        showgrid=True
                                    ),
                                    yaxis=dict(
                                        title=f'{price_column} Price ({currency_symbol})',
                                        titlefont=dict(family='Lato', size=14, color='#f0f4f8'),
                                        tickfont=dict(family='Lato', size=12, color='#f0f4f8'),
                                        gridcolor='rgba(240, 244, 248, 0.2)',
                                        showgrid=True
                                    ),
                                    plot_bgcolor='#0a0a0a',
                                    paper_bgcolor='rgba(10, 10, 10, 0.95)',
                                    showlegend=False,
                                    margin=dict(l=50, r=50, t=80, b=50),
                                    height=400
                                )
                                
                                # Display chart
                                st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error fetching stock price data for {ticker}: {str(e)}. Please check the ticker or try again later.")
                
                # Placeholder for future component (e.g., Financial Metrics)
                elif st.session_state.active_component == "financial_metrics":
                    st.subheader(f"Financial Metrics for {company['name']}")
                    st.write("Placeholder for financial metrics component (to be implemented).")
                    # Add future component logic here, e.g.:
                    # st.write("Display financial data, tables, or charts")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Display matching companies
        st.subheader(f"Companies matching '{search_query}'")
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.markdown('<div class="table-row">', unsafe_allow_html=True)
        cols = st.columns([3, 2, 2])
        headers = ["Company Name", "Sector", "Type"]
        for col, header in zip(cols, headers):
            with col:
                st.markdown(f'<div class="table-cell"><b>{header}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        for company in matching_companies:
            is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))
            st.markdown('<div class="table-row">', unsafe_allow_html=True)
            cols = st.columns([3, 2, 2])
            with cols[0]:
                if st.button(company["name"], key=f"view_{company['id']}"):
                    st.session_state.view_company_details = company["id"]
                    st.session_state.active_component = None  # Reset when selecting a new company
                    st.rerun()
            with cols[1]:
                st.markdown(f'<div class="table-cell">{company["sector"]}</div>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f'<div class="table-cell">{"IPO" if is_ipo else "Regular"}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)