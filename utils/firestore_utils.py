import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("utils/firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Firestore operations
def save_decision(project_id, user_email, ref_id, decision):
    doc_ref = db.collection("projects").document(project_id).collection("decisions").document(f"{ref_id}_{user_email}")
    doc_ref.set({"decision": decision})

def get_decisions(project_id):
    decisions_ref = db.collection("projects").document(project_id).collection("decisions")
    return {doc.id: doc.to_dict() for doc in decisions_ref.stream()}

def save_reference(project_id, ref_id, reference):
    db.collection("projects").document(project_id).collection("references").document(ref_id).set(reference)

def get_references(project_id):
    ref_col = db.collection("projects").document(project_id).collection("references")
    return [doc.to_dict() for doc in ref_col.stream()]

def get_users(project_id):
    return [doc.id for doc in db.collection("projects").document(project_id).collection("users").stream()]

def add_user_to_project(project_id, user_email, role="reviewer"):
    db.collection("projects").document(project_id).collection("users").document(user_email).set({"role": role})

def get_user_role(project_id, user_email):
    doc = db.collection("projects").document(project_id).collection("users").document(user_email).get()
    return doc.to_dict().get("role", "reviewer") if doc.exists else "reviewer"

def transfer_project_ownership(project_id, new_owner_email):
    users_ref = db.collection("projects").document(project_id).collection("users")
    for doc in users_ref.stream():
        users_ref.document(doc.id).set({"role": "reviewer"})
    users_ref.document(new_owner_email).set({"role": "admin"})

# Firebase Web Config (for Google Login)
firebase_web_config = {
    "apiKey": "AIzaSyBxwUgXCEqtRC0oRZbYDJmd07Q7JKC3dqI",
    "authDomain": "metascreenerml.firebaseapp.com",
    "projectId": "metascreenerml",
    "storageBucket": "metascreenerml.appspot.com",
    "messagingSenderId": "1071939977886",
    "appId": "1:1071939977886:web:b356bcf1eea0c2df98fc63"
}

# Project header
def show_project_header():
    project_id = st.session_state.get("project_id")
    if project_id:
        st.markdown(f"### 📌 Project: `{project_id}`")
    else:
        st.warning("⚠️ No project assigned. Please assign one in the Import References page.")
