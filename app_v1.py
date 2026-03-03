import streamlit as st
import os
import io
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from fpdf import FPDF

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Please set it in your environment variables.")

# ---------------------------------------
# Initialize ChatOpenAI (NON-DEPRECATED)
# ---------------------------------------
openai_llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
    temperature=0.7
)

# ---------------------------------------
# Streamlit app setup
# ---------------------------------------
st.set_page_config(
    page_title="AI-Powered Resume and Cover Letter Generator",
    layout="wide"
)

st.markdown("""
# 📝 AI-Powered Cover Letter and Resume Generator  
Developed by Jillani SoftTech 😎  

Generate a professional cover letter or resume with AI assistance.
""")

# ---------------------------------------
# PDF class (SAFE – no font issues)
# ---------------------------------------
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Arial", size=12)

def create_pdf(text):
    pdf = PDF()
    pdf.multi_cell(0, 10, text)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output, 'F')
    pdf_output.seek(0)
    return pdf_output

# ---------------------------------------
# Utility functions
# ---------------------------------------
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def generate_text(prompt):
    try:
        return openai_llm.predict(prompt)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def display_and_download(text, label):
    st.subheader(label)
    st.write(text)

    st.download_button(
        f"Download {label} as TXT",
        text,
        file_name=f"{label}.txt"
    )

    pdf_file = create_pdf(text)
    st.download_button(
        f"Download {label} as PDF",
        pdf_file,
        file_name=f"{label}.pdf",
        mime="application/pdf"
    )

# ---------------------------------------
# Cover Letter UI
# ---------------------------------------
def collect_cover_letter_inputs():
    with st.form("cover_letter_form"):
        res_format = st.radio(
            "Do you want to upload or paste your resume?",
            ("Upload", "Paste")
        )

        resume_text = ""
        if res_format == "Upload":
            res_file = st.file_uploader("📁 Upload your resume in PDF format")
            if res_file:
                resume_text = extract_text_from_pdf(res_file)
        else:
            resume_text = st.text_area("Paste your resume content")

        job_desc = st.text_area("Paste job description")
        user_name = st.text_input("Your name")
        company = st.text_input("Company name")
        manager = st.text_input("Hiring manager")
        role = st.text_input("Job title / role")
        referral = st.text_input("How did you find out about this opportunity?")

        submitted = st.form_submit_button("Generate Cover Letter")

        if submitted and resume_text:
            prompt = f"""
You are an AI assistant that writes professional cover letters.

Candidate Name: {user_name}
Job Role: {role}
Company: {company}
Hiring Manager: {manager}
Referral Source: {referral}

Resume:
{resume_text}

Job Description:
{job_desc}

Instructions:
- Write a professional 3-paragraph cover letter
- Match skills with job description
- Keep a confident but polite tone
"""
            return prompt

    return None

# ---------------------------------------
# Resume UI
# ---------------------------------------
def collect_resume_inputs():
    with st.form("resume_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn Profile URL")
        portfolio = st.text_input("Portfolio URL")

        summary = st.text_area("Professional Summary")
        experience = st.text_area("Work Experience")
        education = st.text_area("Education")
        skills = st.text_area("Skills")
        certifications = st.text_area("Certifications / Awards")
        languages = st.text_area("Languages")
        interests = st.text_area("Interests")

        submitted = st.form_submit_button("Generate Resume")

        if submitted:
            prompt = f"""
Create a professional resume using the following information:

Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
Portfolio: {portfolio}

Summary:
{summary}

Experience:
{experience}

Education:
{education}

Skills:
{skills}

Certifications:
{certifications}

Languages:
{languages}

Interests:
{interests}
"""
            return prompt

    return None

# ---------------------------------------
# Main App
# ---------------------------------------
def main():
    tab1, tab2 = st.tabs(["Cover Letter Generator", "Resume Generator"])

    with tab1:
        st.markdown("### Generate Your Cover Letter")
        prompt = collect_cover_letter_inputs()
        if prompt:
            result = generate_text(prompt)
            if result:
                display_and_download(result, "Cover Letter")

    with tab2:
        st.markdown("### Generate Your Resume")
        prompt = collect_resume_inputs()
        if prompt:
            result = generate_text(prompt)
            if result:
                display_and_download(result, "Resume")

if __name__ == "__main__":
    main()