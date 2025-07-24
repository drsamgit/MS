# utils/firestore_utils.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate("utils/firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

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
    refs = [doc.to_dict() for doc in ref_col.stream()]
    return refs

def get_users(project_id):
    return [doc.id for doc in db.collection("projects").document(project_id).collection("users").stream()]
