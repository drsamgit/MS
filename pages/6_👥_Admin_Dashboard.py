# pages/6_👥_Admin_Dashboard.py
import streamlit as st
from utils.firestore_utils import get_users

st.title("👥 Admin Dashboard")
project_id = st.text_input("Enter Project ID")

if st.button("Fetch Reviewers"):
    users = get_users(project_id)
    st.write("### Reviewers:", users)
