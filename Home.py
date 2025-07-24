import streamlit as st
import requests

FIREBASE_WEB_API_KEY = "AIzaSyBQX6G7pAL09QjoZNBIzuDlpzQ8gpGVZOs"

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

# Session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔄 Safe navigation after login
if st.session_state.get("needs_rerun"):
    st.success("✅ Login successful! You can now continue.")
    st.session_state.needs_rerun = False
    if st.button("➡️ Go to Import References"):
        st.switch_page("📁 Import References")
    st.stop()

# ✅ Already logged in
if st.session_state.logged_in:
    st.success(f"✅ Logged in as {st.session_state.email}")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.success("🔁 Logged out. Please reload or return via sidebar.")
        st.stop()

# 🔐 Login/Signup UI
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
        if st.button("Login"):
            res = firebase_sign_in(email, password)
            if "idToken" in res:
                st.session_state.logged_in = True
                st.session_state.email = res["email"]
                st.session_state.needs_rerun = True
                st.success("Login successful.")
            else:
                st.error(res.get("error", {}).get("message", "Login failed."))

    elif choice == "Forgot Password":
        if st.button("Send Reset Email"):
            res = firebase_send_password_reset(email)
            if "email" in res:
                st.success("Password reset email sent.")
            else:
                st.error(res.get("error", {}).get("message", "Reset failed."))
