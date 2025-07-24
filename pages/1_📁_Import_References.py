import streamlit as st
import pandas as pd
import rispy
from nbib import parse
from utils.firestore_utils import save_reference, show_project_header

st.set_page_config(page_title="Import References")

st.title("📁 Import References")

# Gatekeeper
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from Home page.")
    st.stop()

# Project name
project_id = st.text_input("🔖 Enter or Assign Project Name", value=st.session_state.get("project_id", ""))
if project_id:
    st.session_state.project_id = project_id
    show_project_header()
else:
    st.stop()

# Upload
uploaded_file = st.file_uploader("Upload reference file (.csv, .ris, .nbib)")
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".ris"):
        entries = rispy.load(uploaded_file)
        df = pd.DataFrame(entries)
    elif uploaded_file.name.endswith(".nbib"):
        content = uploaded_file.read().decode("utf-8")
        parsed = list(parse(content))
        df = pd.DataFrame(parsed)
    else:
        st.error("Unsupported file type. Use .csv, .ris, or .nbib")
        df = None

    if df is not None:
        st.success("✅ File loaded successfully.")
        st.dataframe(df.head())
        for i, row in df.iterrows():
            ref_id = f"ref_{i}"
            save_reference(project_id, ref_id, row.to_dict())
        st.session_state[f"refs_{project_id}"] = df.to_dict(orient="records")
        st.success("📤 References saved to Firestore.")

