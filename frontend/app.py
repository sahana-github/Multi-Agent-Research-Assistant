import streamlit as st
import requests

st.title("🔎 Multi-Agent Research Assistant")

user_input = st.text_input("Enter your research question:")
modality = st.selectbox("Select input type:", ["text"])

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/ask", json={
            "user_input": user_input,
            "modality": modality
        })
        if res.status_code == 200:
            response = res.json()["response"]
            st.subheader("🧠 Summary")
            st.write(response)
        else:
            st.error("Failed to get response.")
