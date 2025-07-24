import streamlit as st
import pyrebase
from utils.firestore_utils import add_user_to_project

firebase_config = {
    "apiKey": "AIzaSyBxwUgXCEqtRC0oRZbYDJmd07Q7JKC3dqI",
    "authDomain": "metascreenerml.firebaseapp.com",
    "projectId": "metascreenerml",
    "storageBucket": "metascreenerml.appspot.com",
    "messagingSenderId": "1071939977886",
    "appId": "1:1071939977886:web:b356bcf1eea0c2df98fc63"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.set_page_config(page_title="MetaScreener ML")

st.title("🔐 MetaScreener ML Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success(f"✅ Logged in as {st.session_state.email}")
    project_id = st.text_input("Assign or Enter Project Name", key="project_entry")
    if project_id:
        st.session_state.project_id = project_id
        add_user_to_project(project_id, st.session_state.email)
        st.success(f"You are now assigned to project `{project_id}` as reviewer.")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
    st.markdown("---")
    st.info("Use the sidebar to navigate to any page once project is assigned.")
else:
    choice = st.selectbox("Choose Action", ["Login", "Signup", "Forgot Password"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Account created successfully!")
            except Exception as e:
                st.error(str(e))
    elif choice == "Forgot Password":
        if st.button("Send Reset Email"):
            try:
                auth.send_password_reset_email(email)
                st.success("Password reset email sent")
            except Exception as e:
                st.error(str(e))
    else:  # Login
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Login successful")
                st.experimental_rerun()
            except Exception as e:
                st.error(str(e))
