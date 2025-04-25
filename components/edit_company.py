import streamlit as st
from components.add_company import add_company_form
from components.add_ipo import add_ipo_form

def edit_company_form():
    if "edit_company" not in st.session_state or not st.session_state.edit_company:
        st.error("No company selected for editing. Please go back to View Mode.")
        if st.button("Back to Home"):
            st.session_state.edit_company = None
            st.session_state.edit_mode = False
            st.session_state.add_company_clicked = False
            st.session_state.add_ipo_clicked = False
            st.rerun()
        return

    company = next((c for c in st.session_state.data["companies"] if c["id"] == st.session_state.edit_company), None)
    if not company:
        st.error("Company not found.")
        if st.button("Back to Home"):
            st.session_state.edit_company = None
            st.session_state.edit_mode = False
            st.session_state.add_company_clicked = False
            st.session_state.add_ipo_clicked = False
            st.rerun()
        return

    st.session_state.edit_mode = True
    is_ipo = company.get("is_ipo", bool(company.get("listing_price", 0) > 0))

    if is_ipo:
        st.session_state.add_ipo_clicked = True
        st.session_state.add_company_clicked = False
        add_ipo_form()
    else:
        st.session_state.add_company_clicked = True
        st.session_state.add_ipo_clicked = False
        add_company_form()