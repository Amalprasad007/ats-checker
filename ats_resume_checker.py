import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
import io

# Set up Gemini API
API_KEY = "AIzaSyBokLFzHBiYF_DyIBqV1QYs3VRh_w_9erw"
genai.configure(api_key=API_KEY)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    text = ""
    pdf_data = uploaded_file.read()
    with fitz.open(stream=io.BytesIO(pdf_data), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

import random

def get_ats_feedback(resume_text):
    """Send resume text to Gemini API for ATS analysis with structured, point-wise feedback and dynamic scoring."""
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # Generate a slight variation in scores to prevent static responses
    base_score = random.randint(40, 90)  

    prompt = f"""
    You are an expert in ATS resume evaluation. Analyze the resume below and provide a structured, point-wise report. 
    The score should be dynamic, based on content quality, structure, and keyword optimization.

    **Use this format:**
     

    **✅ Positive Aspects:**  
    - Bullet points are well-structured (if applicable)  
    - Good use of keywords (if applicable)  
    - Clear section headings  

    **⚠️ Areas for Improvement:**  
    - Missing important job-specific keywords  
    - Formatting issues (if detected)  
    - Lack of measurable achievements  

    **💡 Suggestions:**  
    - Add more industry-specific keywords  
    - Improve readability with better spacing  
    - Ensure all contact details are ATS-friendly  

    **Resume Text:**  
    {resume_text}
    """

    response = model.generate_content(prompt)

    return response.text.strip() if hasattr(response, "text") else response




# Streamlit UI
st.set_page_config(page_title="ATS Resume Checker", layout="wide")
st.title("📄 Resume Checker")
st.write("Upload your resume to check its ATS compatibility and receive improvement suggestions.")

uploaded_file = st.file_uploader("Upload your PDF Resume", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)
    
    if st.button("Suggestions & Feedback"):
        st.write("⏳ Analyzing your resume...")
        feedback = get_ats_feedback(resume_text)
        st.subheader("📊 ATS Score & Feedback")
        st.write(feedback)
