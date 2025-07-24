# pages/7_📄_PDF_Viewer.py
import streamlit as st
import base64

st.title("📄 PDF Viewer & Annotation")
uploaded_pdf = st.file_uploader("Upload PDF for a Reference", type="pdf")

if uploaded_pdf:
    pdf_bytes = uploaded_pdf.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)
    annotation = st.text_area("Add notes or tags")
    if st.button("Save Annotation"):
        st.success("Annotation saved (not persisted in demo)")

