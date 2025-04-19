import streamlit as st
from components.add_sector import add_sector_form
from components.add_company import add_company_form
from components.add_ipo import add_ipo_form
from components.view_mode import view_mode
from components.high_return import high_return
from components.hx_cat import hx_cat
from components.invest_companies import invest_companies
from components.visualize_companies import visualize_companies
from components.journal_ledger import journal_ledger
from components.edit_company import edit_company_form
from components.portfolio_dashboard import portfolio_dashboard
from components.utils import load_data
from components.styles import apply_styles

# Set page configuration
st.set_page_config(page_title="Sector-based Stock Tracker", layout="wide")

# Apply custom styles
apply_styles()

# Display images and title in a single row
col1, col2, col3, col4 = st.columns([1, 1, 4, 1])
with col1:
    st.image("assets/bull.png", width=50)
with col2:
    st.image("assets/hoox_logo.png", width=100)
with col3:
    st.markdown("<h1 style='text-align: left; margin-top: 0;'>Companywise Tracker & Analysis</h1>", unsafe_allow_html=True)
with col4:
    st.image("assets/bear.png", width=50)


# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'add_sector_clicked' not in st.session_state:
    st.session_state.add_sector_clicked = False

if 'add_company_clicked' not in st.session_state:
    st.session_state.add_company_clicked = False

if 'add_ipo_clicked' not in st.session_state:
    st.session_state.add_ipo_clicked = False

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = False

if 'selected_sector_for_view' not in st.session_state:
    st.session_state.selected_sector_for_view = None

if 'show_high_return' not in st.session_state:
    st.session_state.show_high_return = False

if 'high_return_sector' not in st.session_state:
    st.session_state.high_return_sector = "All Sectors"

if 'show_hx_cat' not in st.session_state:
    st.session_state.show_hx_cat = False

if 'show_invest_companies' not in st.session_state:
    st.session_state.show_invest_companies = False

if 'invest_companies_sector' not in st.session_state:
    st.session_state.invest_companies_sector = "All Sectors"

if 'show_visualize_companies' not in st.session_state:
    st.session_state.show_visualize_companies = False

if 'visualize_sector' not in st.session_state:
    st.session_state.visualize_sector = "All Sectors"

if 'filter_cap_wise' not in st.session_state:
    st.session_state.filter_cap_wise = False

if 'selected_cap' not in st.session_state:
    st.session_state.selected_cap = "Large-Cap"

if 'filter_combined_caps' not in st.session_state:
    st.session_state.filter_combined_caps = False

if 'show_journal_ledger' not in st.session_state:
    st.session_state.show_journal_ledger = False

if 'edit_company' not in st.session_state:
    st.session_state.edit_company = None

if 'view_company_details' not in st.session_state:
    st.session_state.view_company_details = None

# Helper functions to toggle UI states
def toggle_add_sector():
    st.session_state.add_sector_clicked = not st.session_state.add_sector_clicked
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_add_company():
    st.session_state.add_company_clicked = not st.session_state.add_company_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_add_ipo():
    st.session_state.add_ipo_clicked = not st.session_state.add_ipo_clicked
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_view_mode():
    st.session_state.view_mode = not st.session_state.view_mode
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.view_mode:
        st.session_state.selected_sector_for_view = None

def toggle_high_return():
    st.session_state.show_high_return = not st.session_state.show_high_return
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_high_return:
        st.session_state.high_return_sector = "All Sectors"

def toggle_hx_cat():
    st.session_state.show_hx_cat = not st.session_state.show_hx_cat
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def toggle_invest_companies():
    st.session_state.show_invest_companies = not st.session_state.show_invest_companies
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_invest_companies:
        st.session_state.invest_companies_sector = "All Sectors"

def toggle_visualize_companies():
    st.session_state.show_visualize_companies = not st.session_state.show_visualize_companies
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None
    if st.session_state.show_visualize_companies:
        st.session_state.visualize_sector = "All Sectors"

def toggle_journal_ledger():
    st.session_state.show_journal_ledger = not st.session_state.show_journal_ledger
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.edit_company = None

def go_to_home():
    st.session_state.add_sector_clicked = False
    st.session_state.add_company_clicked = False
    st.session_state.add_ipo_clicked = False
    st.session_state.view_mode = False
    st.session_state.show_high_return = False
    st.session_state.show_hx_cat = False
    st.session_state.show_invest_companies = False
    st.session_state.show_visualize_companies = False
    st.session_state.show_journal_ledger = False
    st.session_state.filter_cap_wise = False
    st.session_state.filter_combined_caps = False
    st.session_state.selected_sector_for_view = None
    st.session_state.edit_company = None
    st.rerun()

# Action buttons
st.markdown("### Actions")
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
with col1:
    if st.button("Home", key="home_button"):
        go_to_home()
with col2:
    if st.button("Add Sector", key="add_sector_button"):
        toggle_add_sector()
with col3:
    if st.button("Add Company", key="add_company_button"):
        toggle_add_company()
with col4:
    if st.button("Add IPOs", key="add_ipo_button"):
        toggle_add_ipo()
with col5:
    if st.button("View Sectors", key="view_mode_button",
                 type="primary" if st.session_state.view_mode else "secondary"):
        toggle_view_mode()
with col6:
    if st.button("High Return", key="high_return_button",
                 type="primary" if st.session_state.show_high_return else "secondary"):
        toggle_high_return()
with col7:
    if st.button("Track-HX-CAT", key="hx_cat_button",
                 type="primary" if st.session_state.show_hx_cat else "secondary"):
        toggle_hx_cat()
with col8:
    if st.button("Track_Invest", key="invest_companies_button",
                 type="primary" if st.session_state.show_invest_companies else "secondary"):
        toggle_invest_companies()
with col9:
    if st.button("Visualize Companies", key="visualize_companies_button",
                 type="primary" if st.session_state.show_visualize_companies else "secondary"):
        toggle_visualize_companies()
with col10:
    if st.button("Journal & Ledger", key="journal_ledger_button",
                 type="primary" if st.session_state.show_journal_ledger else "secondary"):
        toggle_journal_ledger()

st.markdown("---")

# Render components based on session state
if st.session_state.add_sector_clicked:
    add_sector_form()

elif st.session_state.add_company_clicked:
    add_company_form()

elif st.session_state.add_ipo_clicked:
    add_ipo_form()

elif st.session_state.view_mode:
    view_mode()

elif st.session_state.show_high_return:
    high_return()

elif st.session_state.show_hx_cat:
    hx_cat()

elif st.session_state.show_invest_companies:
    invest_companies()

elif st.session_state.show_visualize_companies:
    visualize_companies()

elif st.session_state.show_journal_ledger:
    journal_ledger()

elif st.session_state.edit_company:
    edit_company_form()

else:
    portfolio_dashboard()