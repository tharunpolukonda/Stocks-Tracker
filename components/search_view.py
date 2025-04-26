import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.utils import get_current_stock_price, get_today_return, calculate_profit_loss
from components.score_metrics import score_metrics

def search_view():
    """Display company search results, details, and components (e.g., line chart, financial metrics) triggered by specific buttons."""
    st.markdown('<div class="centered-header"><h2>Search Companies</h2></div>', unsafe_allow_html=True)

    # Get search query from session state
    search_query = st.session_state.search_query.lower().strip()

    if not search_query:
        st.markdown('<div class="detail-box">Please enter a search query to find companies.</div>', unsafe_allow_html=True)
        return

    # Filter companies by search query
    matching_companies = [
        company for company in st.session_state.data["companies"]
        if search_query in company["name"].lower()
    ]

    if not matching_companies:
        st.markdown(f'<div class="detail-box">No companies found matching \'{search_query}\'.</div>', unsafe_allow_html=True)
        return

    # Check if viewing company details
    if st.session_state.view_company_details:
        company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.view_company_details), None)
        if company:
            st.markdown('<div class="company-details-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="centered-header"><h3>Details for {company["name"]}</h3></div>', unsafe_allow_html=True)
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

            # Define fields for main company details
            screener_link = company.get('screener_link', '')
            view_weblink = company.get('view_weblink', '')
            fields = [
                ("Company Name", company["name"]),
                ("Sector", company["sector"]),
                ("Ticker", company["ticker"]),
                ("Type", "IPO" if is_ipo else "Regular"),
                ("Purchase Date", company.get("purchase_date", "N/A")),
                ("Buy Price", f"{currency_symbol}{buy_price:.2f}"),
                ("Shares", str(shares)),
                ("Total Invested", f"{currency_symbol}{total_invested:.2f}"),
                ("Current Price", current_price_display),
                ("Day Change", day_change_display),
                ("P/L", pl_display),
                ("P/L %", pl_percent_display),
                ("Screener Link", f'<a href="{screener_link}">Screener_Link</a>' if screener_link else "N/A"),
                ("View Weblink", f'<a href="{view_weblink}">Web_Link</a>' if view_weblink else "N/A"),
            ]

            # Display main company details in rows of 4
            for i in range(0, len(fields), 4):
                cols = st.columns(4)
                for j, (label, value) in enumerate(fields[i:i+4]):
                    with cols[j]:
                        if label in ["Screener Link", "View Weblink"] and value != "N/A":
                            st.markdown(f'<div class="screener-link">{value}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="detail-box"><b>{label}</b>: {value}</div>', unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)

            if is_ipo:
                st.markdown('<div class="ipo-details-container">', unsafe_allow_html=True)
                st.markdown('<div class="centered-header"><h3>IPO Details</h3></div>', unsafe_allow_html=True)
                
                # Define IPO fields
                pl_listing = ((current_price - company.get('listing_price', 0)) / company.get('listing_price', 0) * 100) if current_price and company.get('listing_price', 0) > 0 else 0.0
                pl_issue = ((current_price - company.get('issue_price', 0)) / company.get('issue_price', 0) * 100) if current_price and company.get('issue_price', 0) > 0 else 0.0
                grow_link = company.get("grow_link", "")
                listed_date_str = company.get('listed_date', '')
                three_month_lip = "N/A"
                six_month_lip = "N/A"
                if listed_date_str and listed_date_str != 'N/A':
                    try:
                        listed_date = datetime.strptime(listed_date_str, "%Y-%m-%d").date()
                        three_month_lip = (listed_date + timedelta(days=90)).strftime("%d-%m-%Y")
                        six_month_lip = (listed_date + timedelta(days=180)).strftime("%d-%m-%Y")
                    except ValueError:
                        pass
                
                ipo_fields = [
                    ("Listing Price", f"{currency_symbol}{company.get('listing_price', 0):.2f}"),
                    ("Issue Price", f"{currency_symbol}{company.get('issue_price', 0):.2f}"),
                    ("P/L % to Listing", f"{pl_listing:.2f}%"),
                    ("Subscription Rate", f"{company.get('subscription_rate', 0)}x"),
                    ("Issue Size", str(company.get('issue_size', 0))),
                    ("Listed Date", company.get('listed_date', 'N/A')),
                    ("Grow Link", f'<a href="{grow_link}">Link</a>' if grow_link else "N/A"),
                    ("P/L % to Issue", f"{pl_issue:.2f}%"),
                    ("3-Month Lock-in (3MLP)", three_month_lip),
                    ("6-Month Lock-in (6MLP)", six_month_lip),
                ]

                # Display IPO details in rows of 4
                for i in range(0, len(ipo_fields), 4):
                    cols = st.columns(4)
                    for j, (label, value) in enumerate(ipo_fields[i:i+4]):
                        with cols[j]:
                            if label == "Grow Link" and value != "N/A":
                                st.markdown(f'<div class="screener-link">{value}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="detail-box"><b>{label}</b>: {value}</div>', unsafe_allow_html=True)
                    st.markdown("<hr>", unsafe_allow_html=True)

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
                    st.markdown(f'<div class="centered-header"><h3>Stock Price History for {company["name"]} (Daily)</h3></div>', unsafe_allow_html=True)
                    
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
                        
                        # Fetch daily stock data with caching
                        @st.cache_data
                        def fetch_stock_data(_ticker, start, end):
                            stock = yf.Ticker(_ticker)
                            return stock.history(start=start, end=end, interval="1d")
                        
                        data = fetch_stock_data(ticker, start_date, end_date)
                        
                        # Debug data
                        st.write(f"Data shape: {data.shape}, Columns: {data.columns}")
                        if not data.empty:
                            st.write(f"Price range: {data.get('Adj Close', data.get('Close')).min()} to {data.get('Adj Close', data.get('Close')).max()}")
                        
                        if data.empty:
                            st.markdown(f'<div class="detail-box">No stock price data available for {ticker}. The company may not have sufficient historical data.</div>', unsafe_allow_html=True)
                        else:
                            # Determine price column: prefer 'Adj Close', fallback to 'Close'
                            price_column = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
                            if price_column not in data.columns:
                                st.markdown(f'<div class="detail-box">No valid price data (\'Adj Close\' or \'Close\') available for {ticker}.</div>', unsafe_allow_html=True)
                            else:
                                # Create line chart
                                fig = go.Figure()
                                
                                # Add glow effect (wider, semi-transparent line)
                                fig.add_trace(
                                    go.Scatter(
                                        x=data.index,
                                        y=data[price_column],
                                        mode='lines',
                                        line=dict(color='#1e90ff', width=5, shape='spline'),
                                        opacity=0.3,
                                        showlegend=False,
                                        hoverinfo='skip'
                                    )
                                )
                                
                                # Add main line
                                fig.add_trace(
                                    go.Scatter(
                                        x=data.index,
                                        y=data[price_column],
                                        mode='lines',
                                        name=price_column,
                                        line=dict(color='#1e90ff', width=3, shape='spline'),
                                        hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: ' + currency_symbol + '%{y:.2f}<extra></extra>'
                                    )
                                )
                                
                                # Add markers for 1-year high and low (only for 1-year period)
                                if time_period == "1 Year" and not data.empty:
                                    high_price = data[price_column].max()
                                    low_price = data[price_column].min()
                                    high_date = data[price_column].idxmax()
                                    low_date = data[price_column].idxmin()
                                    
                                    fig.add_trace(
                                        go.Scatter(
                                            x=[high_date],
                                            y=[high_price],
                                            mode='markers+text',
                                            name='1-Year High',
                                            marker=dict(color='#00FF00', size=10, symbol='circle'),
                                            text=[f'High: {currency_symbol}{high_price:.2f}'],
                                            textposition='top center',
                                            hovertemplate='High: ' + currency_symbol + '%{y:.2f}<br>Date: %{x|%Y-%m-%d}<extra></extra>'
                                        )
                                    )
                                    fig.add_trace(
                                        go.Scatter(
                                            x=[low_date],
                                            y=[low_price],
                                            mode='markers+text',
                                            name='1-Year Low',
                                            marker=dict(color='#FF0000', size=10, symbol='circle'),
                                            text=[f'Low: {currency_symbol}{low_price:.2f}'],
                                            textposition='bottom center',
                                            hovertemplate='Low: ' + currency_symbol + '%{y:.2f}<br>Date: %{x|%Y-%m-%d}<extra></extra>'
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
                                        gridcolor='rgba(30, 144, 255, 0.3)',
                                        tickformat='%Y-%m-%d',
                                        showgrid=True,
                                        showticklabels=True,
                                        visible=True,
                                        showline=True,
                                        linecolor='#f0f4f8',
                                        tickmode='auto',
                                        nticks=10
                                    ),
                                    yaxis=dict(
                                        title=f'{price_column} Price ({currency_symbol})',
                                        titlefont=dict(family='Lato', size=14, color='#f0f4f8'),
                                        tickfont=dict(family='Lato', size=12, color='#f0f4f8'),
                                        gridcolor='rgba(30, 144, 255, 0.3)',
                                        showgrid=True,
                                        showticklabels=True,
                                        visible=True,
                                        showline=True,
                                        linecolor='#f0f4f8',
                                        tickmode='auto'
                                    ),
                                    plot_bgcolor='rgba(10, 10, 10, 0.95)',
                                    paper_bgcolor='rgba(10, 10, 10, 0.95)',
                                    showlegend=True,
                                    legend=dict(
                                        font=dict(family='Lato', size=12, color='#f0f4f8'),
                                        bgcolor='rgba(10, 10, 10, 0.95)',
                                        bordercolor='#1e90ff',
                                        borderwidth=1,
                                        x=0.01,
                                        y=0.99
                                    ),
                                    margin=dict(l=50, r=50, t=80, b=50),
                                    height=500,
                                    hovermode='x unified',
                                    hoverlabel=dict(
                                        bgcolor='rgba(30, 144, 255, 0.9)',
                                        font=dict(family='Lato', size=14, color='#f0f4f8'),
                                        bordercolor='#1e90ff'
                                    )
                                )
                                
                                # Wrap chart in styled container
                                st.markdown('<div class="plotly-chart-container">', unsafe_allow_html=True)
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.markdown(f'<div class="detail-box">Error fetching stock price data for {ticker}: {str(e)}. Please check the ticker or try again later.</div>', unsafe_allow_html=True)
                
                # Financial Metrics: Call score_metrics component
                elif st.session_state.active_component == "financial_metrics":
                    score_metrics(company["ticker"], company["name"])
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Display matching companies
        st.markdown(f'<div class="centered-header"><h3>Companies matching \'{search_query}\'</h3></div>', unsafe_allow_html=True)
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