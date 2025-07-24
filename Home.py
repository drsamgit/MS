import streamlit as st
import requests
import firebase_admin
from firebase_admin import firestore
from utils.firestore_utils import add_user_to_project

FIREBASE_WEB_API_KEY = "AIzaSyBQX6G7pAL09QjoZNBIzuDlpzQ8gpGVZOs"
db = firestore.client()

st.set_page_config(page_title="MetaScreener ML")
st.title("🔐 MetaScreener ML Login")

# Firebase helpers
def firebase_sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    return requests.post(url, json={"email": email, "password": password, "returnSecureToken": True}).json()

def firebase_sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    return requests.post(url, json={"email": email, "password": password, "returnSecureToken": True}).json()

def firebase_send_password_reset(email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    return requests.post(url, json={"requestType": "PASSWORD_RESET", "email": email}).json()

def fetch_user_projects(email):
    project_ids = []
    for doc in db.collection("projects").stream():
        proj_id = doc.id
        members = db.collection("projects").document(proj_id).collection("users").stream()
        if any(m.id == email for m in members):
            project_ids.append(proj_id)
    return project_ids

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# MAIN APP
if st.session_state.logged_in:
    st.success(f"✅ Logged in as {st.session_state.email}")
    user_email = st.session_state.email
    existing_projects = fetch_user_projects(user_email)

    project_choice = st.selectbox("Select a Project or Create New", ["-- Create New Project --"] + existing_projects)

    if project_choice == "-- Create New Project --":
        new_project = st.text_input("🆕 Enter New Project Name")
        if new_project:
            st.session_state.project_id = new_project
            add_user_to_project(new_project, user_email)
            st.success(f"✅ Project `{new_project}` created and assigned.")
    else:
        st.session_state.project_id = project_choice
        st.success(f"✅ Switched to project `{project_choice}`.")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()

else:
    choice = st.selectbox("Choose Action", ["Signup", "Login", "Forgot Password"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            res = firebase_sign_up(email, password)
            if "idToken" in res:
                st.success("✅ Account created! Now log in.")
            else:
                st.error(res.get("error", {}).get("message", "Signup failed."))

    elif choice == "Login":
        st.info("You must sign up first before logging in.")
        if st.button("Login"):
            res = firebase_sign_in(email, password)
            if "idToken" in res:
                st.session_state.logged_in = True
                st.session_state.email = res["email"]
                st.session_state.needs_rerun = True
                st.success("Login successful. Reloading...")

            else:
                st.error(res.get("error", {}).get("message", "Login failed."))

    elif choice == "Forgot Password":
        if st.button("Send Reset Email"):
            res = firebase_send_password_reset(email)
            if "email" in res:
                st.success("Password reset email sent.")
            else:
                st.error(res.get("error", {}).get("message", "Reset failed."))

# ✅ Safe delayed rerun at bottom
import time
if st.session_state.get("needs_rerun"):
    st.session_state.needs_rerun = False
    time.sleep(0.5)
    st.experimental_rerun()
