import streamlit as st
import pandas as pd
import rispy
from utils.firestore_utils import save_reference, show_project_header

st.set_page_config(page_title="Import References")
st.title("📁 Import References")

# 🔐 Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()

# 🔖 Ensure project is assigned
project_id = st.session_state.get("project_id")
if not project_id:
    st.warning("Please select or create a project on the Home page.")
    st.stop()

show_project_header()

uploaded_file = st.file_uploader("📄 Upload reference file (.csv or .ris)")
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
