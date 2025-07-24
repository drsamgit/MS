# pages/6_👥_Admin_Dashboard.py
import streamlit as st
from utils.firestore_utils import get_users, get_references

st.title("👥 Admin Dashboard")
project_id = st.text_input("Enter Project ID")

if st.button("Fetch Reviewers"):
    users = get_users(project_id)
    st.write("### Reviewers:", users)

if st.button("Preview Uploaded References"):
    refs = get_references(project_id)
    if refs:
        st.write("### Sample References:")
        for ref in refs[:5]:
            st.markdown(f"**{ref.get('Title', 'No Title')}**\n\n{ref.get('Abstract', '')}")
    else:
        st.warning("No references found.")
