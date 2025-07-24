import streamlit as st
import requests
from utils.firestore_utils import add_user_to_project

FIREBASE_WEB_API_KEY = "AIzaSyBQX6G7pAL09QjoZNBIzuDlpzQ8gpGVZOs"

st.set_page_config(page_title="MetaScreener ML")
st.title("🔐 MetaScreener ML Login")

def firebase_sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    return requests.post(url, json=payload).json()

def firebase_sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    return requests.post(url, json={"email": email, "password": password, "returnSecureToken": True}).json()

def firebase_send_password_reset(email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    return requests.post(url, json={"requestType": "PASSWORD_RESET", "email": email}).json()

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
else:
    choice = st.selectbox("Choose Action", ["Login", "Signup", "Forgot Password"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            res = firebase_sign_up(email, password)
            if "idToken" in res:
                st.success("Account created successfully!")
            else:
                st.error(res.get("error", {}).get("message", "Signup failed"))

    elif choice == "Forgot Password":
        if st.button("Send Reset Email"):
            res = firebase_send_password_reset(email)
            if "email" in res:
                st.success("Password reset email sent")
            else:
                st.error(res.get("error", {}).get("message", "Error sending reset email"))

    else:  # Login
        if st.button("Login"):
            res = firebase_sign_in(email, password)
            if "idToken" in res:
                st.session_state.logged_in = True
                st.session_state.email = res["email"]
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error(res.get("error", {}).get("message", "Login failed"))

    st.markdown("---")
    st.markdown("👉 Or use [Google login (coming soon)]()")
