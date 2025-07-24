
# pages/8_📊_Project_Stats.py
import streamlit as st
from utils.firestore_utils import get_references, get_decisions

st.title("📊 Project Stats & Dedupe")
project_id = st.text_input("Enter Project ID")

if st.button("Show Stats"):
    refs = get_references(project_id)
    decs = get_decisions(project_id)
    st.write("### Total References:", len(refs))
    st.write("### Decisions Made:", len(decs))
    conflicts = [k for k, v in decs.items() if isinstance(v, dict) and 'conflict' in v.values()]
    st.write("### Conflicts:", len(conflicts))

    # Deduplication: naive check by title match
    titles = [r['Title'].lower().strip() for r in refs if 'Title' in r]
    seen = set()
    duplicates = []
    for t in titles:
        if t in seen:
            duplicates.append(t)
        else:
            seen.add(t)
    st.write("### Duplicates Detected:", len(duplicates))
    if duplicates:
        st.write(duplicates)
