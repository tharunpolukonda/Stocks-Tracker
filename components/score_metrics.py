import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.data = self._fetch_data()
        self.metrics = self._calculate_metrics()
        
    def _fetch_data(self):
        """Fetch and clean data from yfinance"""
        try:
            data = {
                'info': self.stock.info,
                'income_stmt': self.stock.financials,
                'balance_sheet': self.stock.balance_sheet,
                'cash_flow': self.stock.cashflow,
                'quarterly_income_stmt': self.stock.quarterly_financials,
                'quarterly_balance_sheet': self.stock.quarterly_balance_sheet,
                'quarterly_cash_flow': self.stock.quarterly_cashflow,
                'actions': self.stock.actions,
                'history': self.stock.history(period="1y"),
                'recommendations': self.stock.recommendations,
                'institutional_holders': self.stock.institutional_holders
            }
            
            for key in ['income_stmt', 'balance_sheet', 'cash_flow', 'quarterly_income_stmt', 
                       'quarterly_balance_sheet', 'quarterly_cash_flow', 'actions', 
                       'recommendations', 'institutional_holders', 'history']:
                if data[key] is not None and not isinstance(data[key], pd.DataFrame):
                    data[key] = pd.DataFrame(data[key])
                elif data[key] is None:
                    data[key] = pd.DataFrame()
                
                if not data[key].empty:
                    data[key] = data[key].apply(pd.to_numeric, errors='coerce')
            
            return data
        except Exception as e:
            logging.error(f"Could not fetch data for {self.ticker}: {str(e)}")
            return {
                'info': {},
                'income_stmt': pd.DataFrame(),
                'balance_sheet': pd.DataFrame(),
                'cash_flow': pd.DataFrame(),
                'quarterly_income_stmt': pd.DataFrame(),
                'quarterly_balance_sheet': pd.DataFrame(),
                'quarterly_cash_flow': pd.DataFrame(),
                'actions': pd.DataFrame(),
                'history': pd.DataFrame(),
                'recommendations': pd.DataFrame(),
                'institutional_holders': pd.DataFrame()
            }

    def _safe_get(self, data, key, default=np.nan, alt_key=None):
        """Safely get values, ensuring numeric output"""
        try:
            if isinstance(data, (pd.DataFrame, pd.Series)):
                if key in data.index:
                    value = data.loc[key].iloc[0]
                    return float(value) if not pd.isna(value) and np.isfinite(value) else default
                elif alt_key and alt_key in data.index:
                    value = data.loc[alt_key].iloc[0]
                    return float(value) if not pd.isna(value) and np.isfinite(value) else default
            elif isinstance(data, dict):
                value = data.get(key, data.get(alt_key, default))
                return float(value) if not pd.isna(value) and np.isfinite(value) else default
            return default
        except Exception as e:
            logging.warning(f"Failed to get {key} or {alt_key} for {self.ticker}: {str(e)}")
            return default

    def _calculate_metrics(self):
        """Calculate financial metrics"""
        metrics = {}
        info = self.data['info']
        income = self.data['income_stmt']
        balance = self.data['balance_sheet']
        cash = self.data['cash_flow']
        quarterly_income = self.data['quarterly_income_stmt']
        quarterly_balance = self.data['quarterly_balance_sheet']
        quarterly_cash = self.data['quarterly_cash_flow']
        history = self.data['history']
        
        def safely_divide(num, den, default=np.nan):
            try:
                num = float(num) if not pd.isna(num) and np.isfinite(num) else 0
                den = float(den) if not pd.isna(den) and np.isfinite(den) else 0
                result = num / den if den != 0 else default
                return result if np.isfinite(result) else default
            except Exception as e:
                logging.warning(f"Division failed for {self.ticker}: num={num}, den={den}, error={str(e)}")
                return default
        
        def calculate_cagr(start_value, end_value, periods):
            try:
                if start_value > 0 and end_value > 0:
                    return ((end_value / start_value) ** (1 / periods) - 1)
                return np.nan
            except Exception as e:
                logging.warning(f"CAGR calculation failed: {str(e)}")
                return np.nan

        is_inr = self.ticker.endswith(('.NS', '.BO'))
        exchange_rate = 1 if is_inr else 83
        crore_converter = 1e7
        
        # Valuation Metrics
        metrics['pe_ratio'] = self._safe_get(info, 'trailingPE')
        metrics['forward_pe'] = self._safe_get(info, 'forwardPE')
        metrics['peg_ratio'] = self._safe_get(info, 'pegRatio')
        metrics['price_to_sales'] = self._safe_get(info, 'priceToSalesTrailing12Months')
        metrics['price_to_book'] = self._safe_get(info, 'priceToBook')
        metrics['ev_to_ebitda'] = self._safe_get(info, 'enterpriseToEbitda')
        metrics['ev_to_revenue'] = self._safe_get(info, 'enterpriseToRevenue')
        metrics['dividend_yield'] = self._safe_get(info, 'dividendYield')
        market_cap = self._safe_get(info, 'marketCap')
        metrics['market_cap_crores'] = market_cap / crore_converter / exchange_rate if not pd.isna(market_cap) else np.nan
        metrics['enterprise_value'] = self._safe_get(info, 'enterpriseValue')
        
        if not history.empty:
            metrics['current_price'] = history['Close'].iloc[-1] if 'Close' in history.columns else np.nan
            metrics['high_1y'] = history['High'].max() if 'High' in history.columns else np.nan
            metrics['low_1y'] = history['Low'].min() if 'Low' in history.columns else np.nan
        else:
            metrics['current_price'] = np.nan
            metrics['high_1y'] = np.nan
            metrics['low_1y'] = np.nan
        
        book_value = self._safe_get(balance, 'Total Stockholder Equity')
        if pd.isna(book_value):
            book_value = self._safe_get(quarterly_balance, 'Total Stockholder Equity')
        metrics['book_value_crores'] = book_value / crore_converter / exchange_rate if not pd.isna(book_value) else np.nan
        
        fcf = self._safe_get(cash, 'Free Cash Flow')
        ocf = self._safe_get(cash, 'Operating Cash Flow')
        net_income = self._safe_get(income, 'Net Income')
        if pd.isna(net_income):
            net_income = self._safe_get(quarterly_income, 'Net Income')
        revenue = self._safe_get(income, 'Total Revenue')
        if pd.isna(revenue):
            revenue = self._safe_get(quarterly_income, 'Total Revenue')
        tangible_book = self._safe_get(balance, 'Tangible Book Value')
        
        interest_expense = self._safe_get(income, 'Interest Expense', alt_key='Interest Expense Non Operating')
        if pd.isna(interest_expense):
            interest_expense = self._safe_get(quarterly_income, 'Interest Expense', alt_key='Interest Expense Non Operating')
        tax_provision = self._safe_get(income, 'Tax Provision', alt_key='Income Tax Expense')
        if pd.isna(tax_provision):
            tax_provision = self._safe_get(quarterly_income, 'Tax Provision', alt_key='Income Tax Expense')
        ebit = net_income + abs(interest_expense) + tax_provision if not pd.isna([net_income, interest_expense, tax_provision]).any() else np.nan
        if pd.isna(ebit):
            q_net_income = self._safe_get(quarterly_income, 'Net Income')
            q_interest_expense = self._safe_get(quarterly_income, 'Interest Expense', alt_key='Interest Expense Non Operating')
            q_tax_provision = self._safe_get(quarterly_income, 'Tax Provision', alt_key='Income Tax Expense')
            ebit = q_net_income + abs(q_interest_expense) + q_tax_provision if not pd.isna([q_net_income, q_interest_expense, q_tax_provision]).any() else np.nan
        
        dividends = self._safe_get(income, 'Net Income From Continuing Ops')
        
        metrics['fcf_yield'] = safely_divide(fcf, market_cap)
        metrics['ev_to_ebit'] = safely_divide(metrics['enterprise_value'], ebit)
        metrics['price_to_cash_flow'] = safely_divide(market_cap, ocf)
        metrics['dividend_payout_ratio'] = safely_divide(dividends, net_income)
        metrics['price_to_tangible_book'] = safely_divide(market_cap, tangible_book)
        metrics['ev_to_ocf'] = safely_divide(metrics['enterprise_value'], ocf)
        metrics['market_cap_to_revenue'] = safely_divide(market_cap, revenue)
        
        if pd.isna(metrics['peg_ratio']):
            pe_ratio = metrics.get('pe_ratio')
            eps_growth = self._safe_get(info, 'earningsQuarterlyGrowth')
            if pe_ratio and eps_growth and eps_growth != 0:
                metrics['peg_ratio'] = safely_divide(pe_ratio, eps_growth * 100)
        
        # Profitability Metrics
        assets = self._safe_get(balance, 'Total Assets')
        if pd.isna(assets):
            assets = self._safe_get(quarterly_balance, 'Total Assets')
        tangible_assets = self._safe_get(balance, 'Net Tangible Assets')
        if pd.isna(tangible_assets):
            tangible_assets = self._safe_get(quarterly_balance, 'Net Tangible Assets')
        
        equity = self._safe_get(balance, 'Total Stockholder Equity')
        if pd.isna(equity):
            equity = self._safe_get(quarterly_balance, 'Total Stockholder Equity')
        if pd.isna(equity):
            total_liab = self._safe_get(balance, 'Total Liabilities', alt_key='Total Liab')
            if pd.isna(total_liab):
                total_liab = self._safe_get(quarterly_balance, 'Total Liabilities', alt_key='Total Liab')
            equity = assets - total_liab if not pd.isna([assets, total_liab]).any() else np.nan
            logging.info(f"Estimated equity for {self.ticker}: assets={assets}, total_liab={total_liab}, equity={equity}")
        
        current_liabilities = self._safe_get(balance, 'Total Current Liabilities', alt_key='Current Liabilities')
        if pd.isna(current_liabilities):
            current_liabilities = self._safe_get(quarterly_balance, 'Total Current Liabilities', alt_key='Current Liabilities')
            if pd.isna(current_liabilities):
                total_liab = self._safe_get(balance, 'Total Liabilities', alt_key='Total Liab')
                long_term_debt = self._safe_get(balance, 'Long Term Debt')
                if not pd.isna([total_liab, long_term_debt]).any():
                    current_liabilities = total_liab - long_term_debt
                else:
                    total_liab = self._safe_get(quarterly_balance, 'Total Liabilities', alt_key='Total Liab')
                    long_term_debt = self._safe_get(quarterly_balance, 'Long Term Debt')
                    current_liabilities = total_liab - long_term_debt if not pd.isna([total_liab, long_term_debt]).any() else np.nan
            logging.info(f"Current liabilities for {self.ticker}: {current_liabilities}")
        
        capital_employed = assets - current_liabilities if not pd.isna([assets, current_liabilities]).any() else np.nan
        logging.info(f"Capital employed for {self.ticker}: assets={assets}, current_liabilities={current_liabilities}, capital_employed={capital_employed}")
        
        metrics['gross_margin'] = self._safe_get(info, 'grossMargins')
        metrics['operating_margin'] = self._safe_get(info, 'operatingMargins')
        if pd.isna(metrics['operating_margin']):
            operating_income = self._safe_get(income, 'Operating Income')
            if pd.isna(operating_income):
                operating_income = self._safe_get(quarterly_income, 'Operating Income')
            metrics['operating_margin'] = safely_divide(operating_income, revenue)
        metrics['net_profit_margin'] = safely_divide(net_income, revenue)
        metrics['eps'] = self._safe_get(info, 'trailingEps')
        
        metrics['roe'] = self._safe_get(info, 'returnOnEquity')
        if pd.isna(metrics['roe']):
            net_income = self._safe_get(income, 'Net Income')
            equity = self._safe_get(balance, 'Total Stockholder Equity')
            metrics['roe'] = safely_divide(net_income, equity)
            if pd.isna(metrics['roe']):
                q_net_income = self._safe_get(quarterly_income, 'Net Income')
                q_equity = self._safe_get(quarterly_balance, 'Total Stockholder Equity')
                metrics['roe'] = safely_divide(q_net_income, q_equity)
        metrics['roe'] = metrics['roe'] * 100 if not pd.isna(metrics['roe']) else np.nan
        logging.info(f"ROE for {self.ticker}: net_income={net_income}, equity={equity}, roe={metrics['roe']}")
        
        metrics['roce'] = np.nan
        if not quarterly_income.empty and not quarterly_balance.empty:
            q_net_income = self._safe_get(quarterly_income, 'Net Income')
            q_interest_expense = self._safe_get(quarterly_income, 'Interest Expense', alt_key='Interest Expense Non Operating')
            q_tax_provision = self._safe_get(quarterly_income, 'Tax Provision', alt_key='Income Tax Expense')
            q_ebit = q_net_income + abs(q_interest_expense) + q_tax_provision if not pd.isna([q_net_income, q_interest_expense, q_tax_provision]).any() else np.nan
            q_total_assets = self._safe_get(quarterly_balance, 'Total Assets')
            q_current_liabilities = self._safe_get(quarterly_balance, 'Total Current Liabilities', alt_key='Current Liabilities')
            if pd.isna(q_current_liabilities):
                q_total_liab = self._safe_get(quarterly_balance, 'Total Liabilities', alt_key='Total Liab')
                q_long_term_debt = self._safe_get(quarterly_balance, 'Long Term Debt')
                q_current_liabilities = q_total_liab - q_long_term_debt if not pd.isna([q_total_liab, q_long_term_debt]).any() else np.nan
            q_capital_employed = q_total_assets - q_current_liabilities if not pd.isna([q_total_assets, q_current_liabilities]).any() else np.nan
            metrics['roce'] = safely_divide(q_ebit, q_capital_employed) * 100 if not pd.isna([q_ebit, q_capital_employed]).any() else np.nan
            logging.info(f"Quarterly ROCE for {self.ticker}: q_ebit={q_ebit}, q_capital_employed={q_capital_employed}, roce={metrics['roce']}")
        
        if pd.isna(metrics['roce']) and not income.empty and not balance.empty:
            net_income = self._safe_get(income, 'Net Income')
            interest_expense = self._safe_get(income, 'Interest Expense', alt_key='Interest Expense Non Operating')
            tax_provision = self._safe_get(income, 'Tax Provision', alt_key='Income Tax Expense')
            ebit = net_income + abs(interest_expense) + tax_provision if not pd.isna([net_income, interest_expense, tax_provision]).any() else np.nan
            total_assets = self._safe_get(balance, 'Total Assets')
            current_liabilities = self._safe_get(balance, 'Total Current Liabilities', alt_key='Current Liabilities')
            if pd.isna(current_liabilities):
                total_liab = self._safe_get(balance, 'Total Liabilities', alt_key='Total Liab')
                long_term_debt = self._safe_get(balance, 'Long Term Debt')
                current_liabilities = total_liab - long_term_debt if not pd.isna([total_liab, long_term_debt]).any() else np.nan
            capital_employed = total_assets - current_liabilities if not pd.isna([total_assets, current_liabilities]).any() else np.nan
            metrics['roce'] = safely_divide(ebit, capital_employed) * 100 if not pd.isna([ebit, capital_employed]).any() else np.nan
            logging.info(f"Annual ROCE for {self.ticker}: ebit={ebit}, capital_employed={capital_employed}, roce={metrics['roce']}")
        
        metrics['roa'] = safely_divide(net_income, assets)
        metrics['ocf_margin'] = safely_divide(ocf, revenue)
        metrics['ebit_margin'] = safely_divide(ebit, revenue)
        metrics['return_on_tangible_assets'] = safely_divide(net_income, tangible_assets)
        metrics['fcf_margin'] = safely_divide(fcf, revenue)
        
        if not income.empty and 'Net Income' in income.index:
            net_income_series = income.loc['Net Income'].dropna()
            if len(net_income_series) >= 2:
                metrics['net_income_growth'] = safely_divide(
                    net_income_series.iloc[0] - net_income_series.iloc[1],
                    net_income_series.iloc[1]
                )
        elif not quarterly_income.empty and 'Net Income' in quarterly_income.index:
            q_net_income_series = quarterly_income.loc['Net Income'].dropna()
            if len(q_net_income_series) >= 4:
                metrics['net_income_growth'] = safely_divide(
                    q_net_income_series.iloc[0] - q_net_income_series.iloc[3],
                    q_net_income_series.iloc[3]
                )
        
        if not income.empty and 'Total Revenue' in income.index:
            revenue_series = income.loc['Total Revenue'].dropna()
            if len(revenue_series) >= 2:
                metrics['revenue_growth'] = safely_divide(
                    revenue_series.iloc[0] - revenue_series.iloc[1],
                    revenue_series.iloc[1]
                )
        elif not quarterly_income.empty and 'Total Revenue' in quarterly_income.index:
            q_revenue_series = quarterly_income.loc['Total Revenue'].dropna()
            if len(q_revenue_series) >= 4:
                metrics['revenue_growth'] = safely_divide(
                    q_revenue_series.iloc[0] - q_revenue_series.iloc[3],
                    q_revenue_series.iloc[3]
                )
        
        if not income.empty and 'Gross Profit' in income.index:
            gross_profit_series = income.loc['Gross Profit'].dropna()
            if len(gross_profit_series) >= 2:
                metrics['gross_profit_growth'] = safely_divide(
                    gross_profit_series.iloc[0] - gross_profit_series.iloc[1],
                    gross_profit_series.iloc[1]
                )
        
        # Liquidity Metrics
        total_debt = self._safe_get(balance, 'Total Debt', alt_key='Long Term Debt')
        if pd.isna(total_debt):
            total_debt = self._safe_get(quarterly_balance, 'Total Debt', alt_key='Long Term Debt')
        metrics['total_debt_crores'] = total_debt / crore_converter / exchange_rate if not pd.isna(total_debt) else np.nan
        
        metrics['debt_to_equity'] = self._safe_get(info, 'debtToEquity')
        if pd.isna(metrics['debt_to_equity']):
            total_debt = self._safe_get(balance, 'Total Debt', alt_key='Long Term Debt')
            if pd.isna(total_debt):
                total_debt = self._safe_get(quarterly_balance, 'Total Debt', alt_key='Long Term Debt')
            equity = self._safe_get(balance, 'Total Stockholder Equity')
            if pd.isna(equity):
                equity = self._safe_get(quarterly_balance, 'Total Stockholder Equity')
            metrics['debt_to_equity'] = safely_divide(total_debt, equity)
        logging.info(f"Debt-to-Equity for {self.ticker}: total_debt={total_debt}, equity={equity}, debt_to_equity={metrics['debt_to_equity']}")
        
        metrics['interest_coverage'] = safely_divide(ebit, abs(interest_expense))
        metrics['ocf_to_debt'] = safely_divide(ocf, total_debt)
        
        receivables = self._safe_get(balance, 'Net Receivables')
        if pd.isna(receivables):
            receivables = self._safe_get(quarterly_balance, 'Net Receivables')
        payables = self._safe_get(balance, 'Accounts Payable')
        if pd.isna(payables):
            payables = self._safe_get(quarterly_balance, 'Accounts Payable')
        cost_of_revenue = self._safe_get(income, 'Cost Of Revenue')
        if pd.isna(cost_of_revenue):
            cost_of_revenue = self._safe_get(quarterly_income, 'Cost Of Revenue')
        metrics['cash_conversion_cycle'] = safely_divide(receivables + 0 - payables, cost_of_revenue / 365)
        
        # Growth Metrics
        metrics['eps_growth'] = self._safe_get(info, 'earningsQuarterlyGrowth')
        
        if not income.empty and 'Total Revenue' in income.index:
            revenue_series = income.loc['Total Revenue'].dropna()
            if len(revenue_series) >= 3:
                metrics['revenue_cagr_3y'] = calculate_cagr(revenue_series.iloc[-1], revenue_series.iloc[0], 3)
        
        if not cash.empty and 'Capital Expenditure' in cash.index:
            capex_series = cash.loc['Capital Expenditure'].dropna()
            if len(capex_series) >= 2:
                metrics['capex_growth'] = safely_divide(capex_series.iloc[0] - capex_series.iloc[1], abs(capex_series.iloc[1]))
        
        if not income.empty and 'Operating Income' in income.index:
            operating_income_series = income.loc['Operating Income'].dropna()
            if len(operating_income_series) >= 2:
                metrics['operating_income_growth'] = safely_divide(
                    operating_income_series.iloc[0] - operating_income_series.iloc[1],
                    operating_income_series.iloc[1]
                )
        
        if not cash.empty and 'Free Cash Flow' in cash.index:
            fcf_series = cash.loc['Free Cash Flow'].dropna()
            if len(fcf_series) >= 2:
                metrics['fcf_growth'] = safely_divide(fcf_series.iloc[0] - fcf_series.iloc[1], fcf_series.iloc[1])
        
        metrics = {k: v for k, v in metrics.items() if not pd.isna(v) and np.isfinite(v)}
        
        for key in ['roe', 'roce', 'debt_to_equity']:
            if key not in metrics or pd.isna(metrics[key]):
                logging.warning(f"Metric {key} is N/A for {self.ticker}")
        
        return metrics

    def _calculate_scores(self):
        """Calculate scores for metrics"""
        scores = {
            'total_score': 0,
            'category_scores': {
                'valuation': 0,
                'profitability': 0,
                'growth': 0,
                'liquidity': 0
            },
            'strengths': [],
            'weaknesses': [],
            'valuation_grade': 'N/A',
            'growth_grade': 'N/A',
            'financial_health': 'N/A'
        }
        
        try:
            metric_categories = {
                'valuation': [
                    ('pe_ratio', 'lower', 20, 30),
                    ('forward_pe', 'lower', 15, 25),
                    ('peg_ratio', 'lower', 1, 2),
                    ('price_to_sales', 'lower', 2, 4),
                    ('price_to_book', 'lower', 1.5, 3),
                    ('ev_to_ebitda', 'lower', 10, 15),
                    ('ev_to_revenue', 'lower', 2, 4),
                    ('dividend_yield', 'higher', 0.01, 0.03),
                    ('fcf_yield', 'higher', 0.02, 0.05),
                    ('ev_to_ebit', 'lower', 15, 25),
                    ('price_to_cash_flow', 'lower', 10, 20),
                    ('dividend_payout_ratio', 'lower', 0.5, 0.8),
                    ('price_to_tangible_book', 'lower', 1.5, 3),
                    ('ev_to_ocf', 'lower', 15, 25),
                    ('market_cap_to_revenue', 'lower', 2, 4)
                ],
                'profitability': [
                    ('gross_margin', 'higher', 0.25, 0.4),
                    ('operating_margin', 'higher', 0.1, 0.15),
                    ('net_profit_margin', 'higher', 0.05, 0.1),
                    ('roe', 'higher', 12, 18),
                    ('roa', 'higher', 0.03, 0.07),
                    ('eps', 'higher', 10, 20),
                    ('fcf_margin', 'higher', 0.02, 0.05),
                    ('roce', 'higher', 15, 20),
                    ('ocf_margin', 'higher', 0.1, 0.2),
                    ('ebit_margin', 'higher', 0.1, 0.2),
                    ('return_on_tangible_assets', 'higher', 0.03, 0.07),
                    ('net_income_growth', 'higher', 0.03, 0.08),
                    ('gross_profit_growth', 'higher', 0.03, 0.08)
                ],
                'growth': [
                    ('eps_growth', 'higher', 0.03, 0.08),
                    ('revenue_growth', 'higher', 0.03, 0.08),
                    ('revenue_cagr_3y', 'higher', 0.03, 0.08),
                    ('capex_growth', 'higher', 0.03, 0.08),
                    ('operating_income_growth', 'higher', 0.03, 0.08),
                    ('fcf_growth', 'higher', 0.03, 0.08),
                    ('net_income_growth', 'higher', 0.03, 0.08)
                ],
                'liquidity': [
                    ('debt_to_equity', 'lower', 0.5, 1.0),
                    ('interest_coverage', 'higher', 3, 5),
                    ('ocf_to_debt', 'higher', 0.2, 0.5),
                    ('cash_conversion_cycle', 'lower', 60, 90)
                ]
            }
            
            total_metrics = 0
            total_score = 0
            
            for category, metrics_list in metric_categories.items():
                category_score = 0
                metrics_count = 0
                
                for metric, direction, good_threshold, great_threshold in metrics_list:
                    value = self.metrics.get(metric, np.nan)
                    if pd.isna(value) or not np.isfinite(value):
                        logging.warning(f"Skipping invalid metric {metric}: {value} for {self.ticker}")
                        continue
                    
                    if direction == 'higher':
                        if value >= great_threshold:
                            score = 100
                        elif value >= good_threshold:
                            score = 75
                        else:
                            score = 50
                    else:
                        if value <= good_threshold:
                            score = 100
                        elif value <= great_threshold:
                            score = 75
                        else:
                            score = 50
                            
                    if score >= 75:
                        scores['strengths'].append(f"{metric}: {value:.2f}")
                    elif score <= 50:
                        scores['weaknesses'].append(f"{metric}: {value:.2f}")
                    
                    category_score += score
                    metrics_count += 1
                    total_score += score
                    total_metrics += 1
                
                if metrics_count > 0:
                    scores['category_scores'][category] = category_score / metrics_count
                else:
                    scores['category_scores'][category] = np.nan
                    logging.warning(f"No valid metrics for category {category} for {self.ticker}")
            
            if total_metrics > 0:
                scores['total_score'] = total_score / total_metrics
            else:
                logging.warning(f"No valid metrics available for scoring for {self.ticker}")
                scores['total_score'] = np.nan
            
            def get_grade(score):
                if pd.isna(score) or not np.isfinite(score):
                    return 'N/A'
                if score >= 90:
                    return 'A'
                elif score >= 80:
                    return 'B'
                elif score >= 70:
                    return 'C'
                elif score >= 60:
                    return 'D'
                else:
                    return 'F'
            
            scores['valuation_grade'] = get_grade(scores['category_scores']['valuation'])
            scores['growth_grade'] = get_grade(scores['category_scores']['growth'])
            scores['financial_health'] = get_grade(scores['category_scores']['liquidity'])
            
        except Exception as e:
            logging.error(f"Scoring failed for {self.ticker}: {str(e)}")
        
        return scores

    def analyze(self):
        """Generate analysis report"""
        try:
            score_card = self._calculate_scores()
            return {
                'ticker': self.ticker,
                'metrics': self.metrics,
                'score': score_card['total_score'],
                'category_scores': score_card['category_scores'],
                'strengths': score_card['strengths'],
                'weaknesses': score_card['weaknesses'],
                'valuation': f"{score_card['valuation_grade']} (P/E: {self.metrics.get('pe_ratio', np.nan):.1f})",
                'growth_grade': score_card['growth_grade'],
                'financial_health': score_card['financial_health']
            }
        except Exception as e:
            logging.error(f"Error generating report for {self.ticker}: {str(e)}")
            return {
                'ticker': self.ticker,
                'error': str(e)
            }

def score_metrics(ticker, company_name):
    """Display financial metrics and scores in Streamlit with enhanced styling."""
    tickercode = ticker.replace('.NS', '').replace('.BO', '')
    
    st.markdown('<div class="screener-link">Screener Link</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box">Ticker Code: {tickercode}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="centered-header"><h2>Financial Metrics for {company_name} ({ticker})</h2></div>', unsafe_allow_html=True)
    
    try:
        analyzer = StockAnalyzer(ticker)
        result = analyzer.analyze()
        
        if 'error' in result:
            st.error(f"Failed to analyze financial metrics for {ticker}: {result['error']}")
            return
        
        if not result['metrics']:
            st.warning(f"Limited financial data available for {ticker}. Some metrics may be unavailable.")
        
        currency_symbol = "₹" if ticker.endswith(('.NS', '.BO')) else "$"
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="centered-header"><h3>Overall Analysis</h3></div>', unsafe_allow_html=True)
        total_score = result.get('score', np.nan)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Score", f"{total_score:.1f}/100" if not pd.isna(total_score) else "N/A")
        with col2:
            st.metric("Valuation Grade", result.get('valuation', 'N/A'))
        with col3:
            st.metric("Growth Grade", result.get('growth_grade', 'N/A'))
        with col4:
            st.metric("Financial Health", result.get('financial_health', 'N/A'))
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="centered-header"><h3>Category Scores</h3></div>', unsafe_allow_html=True)
        category_scores = result.get('category_scores', {})
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valuation", f"{category_scores.get('valuation', np.nan):.1f}" if not pd.isna(category_scores.get('valuation')) else "N/A")
        with col2:
            st.metric("Profitability", f"{category_scores.get('profitability', np.nan):.1f}" if not pd.isna(category_scores.get('profitability')) else "N/A")
        with col3:
            st.metric("Growth", f"{category_scores.get('growth', np.nan):.1f}" if not pd.isna(category_scores.get('growth')) else "N/A")
        with col4:
            st.metric("Liquidity", f"{category_scores.get('liquidity', np.nan):.1f}" if not pd.isna(category_scores.get('liquidity')) else "N/A")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="centered-header"><h3>Requested Metrics</h3></div>', unsafe_allow_html=True)
        metrics = result.get('metrics', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="sector-header">Valuation & Market</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Market Cap: {currency_symbol}{metrics.get("market_cap_crores", np.nan):,.2f} Cr</div>' if not pd.isna(metrics.get('market_cap_crores')) else '<div class="metric-box">Market Cap: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Current Price: {currency_symbol}{metrics.get("current_price", np.nan):.2f}</div>' if not pd.isna(metrics.get('current_price')) else '<div class="metric-box">Current Price: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">1-Year High/Low: {currency_symbol}{metrics.get("high_1y", np.nan):.2f}/{metrics.get("low_1y", np.nan):.2f}</div>' if not pd.isna(metrics.get('high_1y')) else '<div class="metric-box">1-Year High/Low: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Book Value: {currency_symbol}{metrics.get("book_value_crores", np.nan):,.2f} Cr</div>' if not pd.isna(metrics.get('book_value_crores')) else '<div class="metric-box">Book Value: N/A</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="sector-header">Growth & Profitability</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Profit Growth: {metrics.get("net_income_growth", np.nan):.2%}</div>' if not pd.isna(metrics.get('net_income_growth')) else '<div class="metric-box">Profit Growth: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Sales Growth: {metrics.get("revenue_growth", np.nan):.2%}</div>' if not pd.isna(metrics.get('revenue_growth')) else '<div class="metric-box">Sales Growth: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">OPM: {metrics.get("operating_margin", np.nan):.2%}</div>' if not pd.isna(metrics.get('operating_margin')) else '<div class="metric-box">OPM: N/A</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="sector-header">Debt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Total Debt: {currency_symbol}{metrics.get("total_debt_crores", np.nan):,.2f} Cr</div>' if not pd.isna(metrics.get('total_debt_crores')) else '<div class="metric-box">Total Debt: N/A</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="centered-header"><h3>Key Metrics</h3></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="sector-header">Valuation & Profitability</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">P/E Ratio: {metrics.get("pe_ratio", np.nan):.2f}</div>' if not pd.isna(metrics.get('pe_ratio')) else '<div class="metric-box">P/E Ratio: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">PEG Ratio: {metrics.get("peg_ratio", np.nan):.2f}</div>' if not pd.isna(metrics.get('peg_ratio')) else '<div class="metric-box">PEG Ratio: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">ROE: {metrics.get("roe", np.nan):.2f}%</div>' if not pd.isna(metrics.get('roe')) else '<div class="metric-box">ROE: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">ROCE: {metrics.get("roce", np.nan):.2f}%</div>' if not pd.isna(metrics.get('roce')) else '<div class="metric-box">ROCE: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Net Profit Margin: {metrics.get("net_profit_margin", np.nan):.2%}</div>' if not pd.isna(metrics.get('net_profit_margin')) else '<div class="metric-box">Net Profit Margin: N/A</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="sector-header">Liquidity & Debt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Debt-to-Equity: {metrics.get("debt_to_equity", np.nan):.2f}</div>' if not pd.isna(metrics.get('debt_to_equity')) else '<div class="metric-box">Debt-to-Equity: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Interest Coverage: {metrics.get("interest_coverage", np.nan):.2f}</div>' if not pd.isna(metrics.get('interest_coverage')) else '<div class="metric-box">Interest Coverage: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Cash Conversion Cycle: {metrics.get("cash_conversion_cycle", np.nan):.1f} days</div>' if not pd.isna(metrics.get('cash_conversion_cycle')) else '<div class="metric-box">Cash Conversion Cycle: N/A</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="sector-header">Growth</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">Revenue Growth: {metrics.get("revenue_growth", np.nan):.2%}</div>' if not pd.isna(metrics.get('revenue_growth')) else '<div class="metric-box">Revenue Growth: N/A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box">FCF Growth: {metrics.get("fcf_growth", np.nan):.2%}</div>' if not pd.isna(metrics.get('fcf_growth')) else '<div class="metric-box">FCF Growth: N/A</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="centered-header"><h3>Strengths and Weaknesses</h3></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="sector-header">Strengths</div>', unsafe_allow_html=True)
            strengths = result.get('strengths', [])
            if not strengths and result['metrics']:
                st.markdown('<div class="strength-box">No strengths identified (limited data)</div>', unsafe_allow_html=True)
            else:
                for s in strengths:
                    st.markdown(f'<div class="strength-box">{s}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="sector-header">Weaknesses</div>', unsafe_allow_html=True)
            weaknesses = result.get('weaknesses', [])
            if not weaknesses and result['metrics']:
                st.markdown('<div class="weakness-box">No weaknesses identified (limited data)</div>', unsafe_allow_html=True)
            else:
                for w in weaknesses:
                    st.markdown(f'<div class="weakness-box">{w}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error analyzing financial metrics for {ticker}: {str(e)}. Please try again later.")