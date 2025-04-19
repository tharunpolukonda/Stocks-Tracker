import streamlit as st
from components.utils import save_data

def add_sector_form():
    st.subheader("Add New Sector")
    with st.form("add_sector_form"):
        sector_name = st.text_input("Sector Name", placeholder="e.g. Technology")
        submit_sector = st.form_submit_button("Add Sector")

        if submit_sector and sector_name:
            if sector_name not in st.session_state.data["sectors"]:
                st.session_state.data["sectors"].append(sector_name)
                save_data(st.session_state.data)
                st.success(f"Sector '{sector_name}' added successfully!")
                st.session_state.add_sector_clicked = False
                st.rerun()
            else:
                st.error(f"Sector '{sector_name}' already exists!")