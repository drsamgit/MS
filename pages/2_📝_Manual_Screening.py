# pages/2_📝_Manual_Screening.py
import streamlit as st
from utils.firestore_utils import get_references, save_decision

st.title("📝 Manual Screening")
project_id = st.text_input("Enter Project ID")
user_email = st.text_input("Enter Your Email")

refs = get_references(project_id)
if not refs:
    st.warning("No references found for this project.")
else:
    index = st.session_state.get('current_index', 0)
    if index < len(refs):
        ref = refs[index]
        st.subheader(ref.get("Title", "No Title"))
        st.write(ref.get("Abstract", "No Abstract"))

        col1, col2, col3 = st.columns(3)
        if col1.button("Include"):
            save_decision(project_id, user_email, f"ref_{index}", 1)
            st.session_state['current_index'] = index + 1
        if col2.button("Exclude"):
            save_decision(project_id, user_email, f"ref_{index}", 0)
            st.session_state['current_index'] = index + 1
        if col3.button("Maybe"):
            save_decision(project_id, user_email, f"ref_{index}", -1)
            st.session_state['current_index'] = index + 1
    else:
        st.success("Screening complete")
