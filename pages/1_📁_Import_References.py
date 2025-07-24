import streamlit as st
import pandas as pd
import rispy
from utils.firestore_utils import save_reference, show_project_header, add_user_to_project
import firebase_admin
from firebase_admin import firestore

db = firestore.client()

st.set_page_config(page_title="Import References")
st.title("📁 Import References")

# 🔐 Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the Home page.")
    st.stop()

email = st.session_state.email
existing_projects = []

# 🔍 Find all projects this user is part of
projects_col = db.collection("projects")
for doc in projects_col.stream():
    proj_id = doc.id
    members = db.collection("projects").document(proj_id).collection("users").stream()
    if any(m.id == email for m in members):
        existing_projects.append(proj_id)

project_choice = st.selectbox("Select a Project or Create New", ["-- Create New Project --"] + existing_projects)

if project_choice == "-- Create New Project --":
    new_proj = st.text_input("🆕 Enter New Project Name")
    if new_proj:
        st.session_state.project_id = new_proj
        add_user_to_project(new_proj, email)
        st.success(f"✅ Project `{new_proj}` created and assigned.")
else:
    st.session_state.project_id = project_choice
    st.success(f"✅ Switched to project `{project_choice}`.")

# ✅ Show current project
if "project_id" not in st.session_state:
    st.stop()

project_id = st.session_state.project_id
show_project_header()

# 📄 Upload references
uploaded_file = st.file_uploader("Upload reference file (.csv or .ris)")
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
        st.success("✅ File loaded successfully")
        st.dataframe(df.head())
        for i, row in df.iterrows():
            ref_id = f"ref_{i}"
            save_reference(project_id, ref_id, row.to_dict())
        st.session_state[f"refs_{project_id}"] = df.to_dict(orient="records")
        st.success("📤 References saved to Firestore")
