# pages/3_🤖_ML_Screener.py
import streamlit as st
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.firestore_utils import get_references, get_decisions, save_decision

st.title("🤖 ML-Assisted Screening")
project_id = st.text_input("Enter Project ID")
user_email = st.text_input("Enter Your Email")

if st.button("Load References"):
    st.session_state[f"refs_{project_id}"] = get_references(project_id)

refs = st.session_state.get(f"refs_{project_id}", [])
decisions = get_decisions(project_id)

if not refs or not decisions:
    st.warning("Insufficient data to train ML model. Click 'Load References' if needed.")
else:
    labeled_data = [(int(k.split('_')[0].split('ref_')[1]), v['decision']) for k, v in decisions.items() if user_email in k]
    if not labeled_data:
        st.info("No labels by this user yet.")
    else:
        indices, y = zip(*labeled_data)
        X_text = [refs[i]['Title'] + " " + str(refs[i].get('Abstract', '')) for i in indices]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(X_text)

        clf = SGDClassifier(loss='log_loss')
        clf.fit(X, y)

        st.subheader("Model Predictions")
        for i, ref in enumerate(refs):
            key = f"ref_{i}_{user_email}"
            if key not in decisions:
                text = ref['Title'] + " " + str(ref.get('Abstract', ''))
                x_pred = vectorizer.transform([text])
                prob = clf.predict_proba(x_pred)[0][1]
                st.write(f"**{ref['Title']}**")
                st.write(f"Prediction Score: {prob:.2f}")
                if st.button(f"Include {i}"):
                    save_decision(project_id, user_email, f"ref_{i}", 1)
                if st.button(f"Exclude {i}"):
                    save_decision(project_id, user_email, f"ref_{i}", 0)
