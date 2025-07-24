# pages/1_📁_Import_References.py
import streamlit as st
import pandas as pd
import rispy
import json
from utils.firestore_utils import save_reference

st.title("📁 Import References")
project_id = st.text_input("Enter Project ID")
uploaded_file = st.file_uploader("Upload reference file (CSV, RIS, NBIB)")

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".ris"):
        entries = rispy.load(uploaded_file)
        df = pd.DataFrame(entries)
    elif uploaded_file.name.endswith(".nbib"):
        content = uploaded_file.read().decode("utf-8")
        from nbib import parse
        parsed = list(parse(content))
        df = pd.DataFrame(parsed)
    else:
        st.error("Unsupported file type")
        df = None

    if df is not None:
        st.success("File loaded successfully")
        st.dataframe(df.head())
        for i, row in df.iterrows():
            ref_id = f"ref_{i}"
            save_reference(project_id, ref_id, row.to_dict())
        st.success("References saved to Firestore")
