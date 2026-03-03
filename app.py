import streamlit as st
from hf_generator import generate_text
from offline_generator import offline_resume, offline_cover_letter
from pdf_utils import generate_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CareerForge",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
h1, h2, h3 {
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("AI powered - Resume/Cover Letter Tool")
option = st.sidebar.radio(
    "Choose Document",
    ["📄 Resume Generator", "✉️ Cover Letter Generator"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    # "✔ AI + Offline Safe\n\n"
    "✔ ATS-friendly output\n\n"
    "✔ PDF & TXT download"
)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>📄CareerForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Smart • Job-Targeted • AI Tool</p>", unsafe_allow_html=True)

st.divider()

# ---------------- COMMON INPUTS ----------------
with st.container():
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Basic Information")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

    with col2:
        location = st.text_input("Location")
        role = st.text_input("Target Job Role")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RESUME ----------------
if option.startswith("📄"):
    with st.container():
        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧾 Resume Details")

        skills = st.text_area("Skills (comma separated)")
        experience = st.text_area("Experience")
        projects = st.text_area("Projects")
        education = st.text_area("Education")

        generate = st.button("✨ Generate Resume", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if generate:
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "role": role,
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "education": education
        }

        with st.spinner("Crafting your resume..."):
            prompt = f"Create a professional ATS-friendly resume for {name} applying for {role}"
            ai_output = generate_text(prompt)

            if ai_output:
                output = ai_output
                st.success("✅ Resume generated using AI")
            else:
                output = offline_resume(data)

        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📄 Generated Resume")
        st.text_area("", output, height=350)
        pdf = generate_pdf(output, "Resume")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download TXT", output, file_name="resume.txt")
        with col2:
            st.download_button("📄 Download PDF", open(pdf, "rb"), file_name="resume.pdf")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- COVER LETTER ----------------
else:
    with st.container():
        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("✉️ Cover Letter Details")

        skills = st.text_area("Key Skills")
        experience = st.text_area("Relevant Experience")
        projects = st.text_area("Projects")

        generate = st.button("✨ Generate Cover Letter", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if generate:
        data = {
            "name": name,
            "role": role,
            "skills": skills,
            "experience": experience,
            "projects": projects
        }

        with st.spinner("Writing your cover letter..."):
            prompt = f"Write a professional cover letter for {name} applying for {role}"
            ai_output = generate_text(prompt)

            if ai_output:
                output = ai_output
                st.success("✅ Cover letter generated using AI")
            else:
                output = offline_cover_letter(data)
                st.warning("⚠️ AI unavailable. Generated offline cover letter.")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("✉️ Generated Cover Letter")
        st.text_area("", output, height=350)
        pdf = generate_pdf(output, "Cover_Letter")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download TXT", output, file_name="cover_letter.txt")
        with col2:
            st.download_button("📄 Download PDF", open(pdf, "rb"), file_name="cover_letter.pdf")

        st.markdown("</div>", unsafe_allow_html=True)