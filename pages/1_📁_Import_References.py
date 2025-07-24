import streamlit as st
import pandas as pd
import rispy
from utils.firestore_utils import save_reference, show_project_header

st.set_page_config(page_title="Import References")
st.title("📁 Import References")

# ✅ Gatekeeper
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the Home page.")
    st.stop()

email = st.session_state.email
existing_projects = []

# 🔍 Find all projects this user is part of
import firebase_admin
from firebase_admin import firestore
db = firestore.client()

projects_col = db.collection("projects")
for doc in projects_col.stream():
    proj_id = doc.id
    members = db.collection("projects").document(proj_id).collection("users").stream()
    if any(m.id == email for m in members):
        existing_projects.append(proj_id)

selected_project = st.selectbox("Select a Project", options=["-- Create New Project --"] + existing_projects)

if selected_project == "-- Create New Project --":
    new_proj = st.text_input("Enter New Project Name")
    if new_proj:
        st.session_state.project_id = new_proj
else:
    st.session_state.project_id = selected_project

# ✅ Show header once assigned
if "project_id" not in st.session_state:
    st.stop()

project_id = st.session_state.project_id
show_project_header()

# 🔼 Upload file
uploaded_file = st.file_uploader("Upload reference file (.csv or .ris only)")
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".ris"):
        entries = rispy.load(uploaded_file)
        df = pd.DataFrame(entries)
    else:
        st.error("Unsupported file type. Use .csv or .ris")
        df = None

    if df is not None:
        st.success("✅ File loaded successfully.")
        st.dataframe(df.head())
        for i, row in df.iterrows():
            ref_id = f"ref_{i}"
            save_reference(project_id, ref_id, row.to_dict())
        st.session_state[f"refs_{project_id}"] = df.to_dict(orient="records")
        st.success("📤 References saved to Firestore.")
