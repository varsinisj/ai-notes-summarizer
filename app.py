import streamlit as st
import fitz 
import google.generativeai as genai
import os


GOOGLE_API_KEY = "AIzaSyBCKtuZZQbLhvZlpXF-w27TCPhGk4EeOBg"
genai.configure(api_key=GOOGLE_API_KEY)

try:
    
    model_name_to_use = "gemini-1.5-flash-001" 
    model = genai.GenerativeModel(model_name=model_name_to_use)
except Exception as e:
    st.error(f"Model initialization failed: {e}. Please ensure '{model_name_to_use}' is available for your API key and region.")
    st.stop()

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_text(text):
    prompt = f"Summarize this in simple bullet points:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

st.title("🧠 AI Notes Summarizer")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.text_area("📄 Extracted Text", extracted_text, height=300)

    if st.button("Summarize Notes"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_text(extracted_text)
                st.subheader("📚 Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"An error occurred while summarizing: {e}")