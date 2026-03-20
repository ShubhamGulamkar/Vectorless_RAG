import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Vectorless RAG System")

st.header("Upload Document")

uploaded_file = st.file_uploader("Upload TXT Document")

if uploaded_file and st.button("Upload"):
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{API_URL}/upload", files={"file": uploaded_file})
    st.success("Document uploaded successfully")

st.header("Ask Question")

question = st.text_input("Enter your question")

if st.button("Search"):
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    data = response.json()

    st.subheader("Answer")
    st.write(data["answer"])