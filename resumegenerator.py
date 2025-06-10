import streamlit as st
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from google.generativeai import configure, GenerativeModel

# --- CONFIGURE GEMINI API ---
GEMINI_API_KEY = "AIzaSyBUjbvHg9nj8l3Fzeb6pL2wcaEv5eRObwY"
MODEL_NAME = "gemini-2.0-flash"
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel(MODEL_NAME)

# --- Function to generate resume using Gemini ---
def generate_resume(name, contact, skills, education, experience, certifications, additional_info, job_role):
    prompt = f"""
    You are an expert resume writer. Generate a professionally formatted resume for the following individual, customized for the role of {job_role}. 

    Name: {name}
    Contact Information: {contact}
    Skills: {skills}
    Education: {education}
    Work Experience: {experience}
    Certifications / Projects: {certifications}
    Additional Information: {additional_info}

    Please format the resume clearly with sections and proper headings.
    """

    response = model.generate_content(prompt)
    return response.text

# --- Function to create PDF ---
def create_pdf(resume_text):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    text_object = p.beginText(40, 800)
    text_object.setFont("Helvetica", 12)

    for line in resume_text.split('\n'):
        text_object.textLine(line)

    p.drawText(text_object)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

# --- Streamlit App ---
st.title("📄 AI-Powered Resume Generator")
st.write("Fill in the details below to generate a professional resume customized for your target job role.")

# --- Form for User Input ---
with st.form("resume_form"):
    name = st.text_input("Full Name")
    contact = st.text_input("Contact Information (Email, Phone, LinkedIn, etc.)")
    skills = st.text_area("Skills (comma-separated)")
    education = st.text_area("Education")
    experience = st.text_area("Work Experience")
    certifications = st.text_area("Certifications / Projects")
    additional_info = st.text_area("Additional Information (Languages, Hobbies, etc.)")
    job_role = st.selectbox(
        "Target Job Role",
        ["Software Engineer", "Data Analyst", "Marketing Manager", "Project Manager", "Product Manager", "Graphic Designer", "Business Analyst", "Other"]
    )

    submitted = st.form_submit_button("Generate Resume")

# --- Handle Resume Generation ---
if submitted or st.session_state.get("resume_generated", False):
    if submitted:
        st.session_state.resume_text = generate_resume(
            name, contact, skills, education, experience, certifications, additional_info, job_role
        )
        st.session_state.resume_generated = True

    st.subheader("Generated Resume:")
    st.text_area("Resume Preview", st.session_state.resume_text, height=400)

    pdf_buffer = create_pdf(st.session_state.resume_text)

    st.download_button(
        label="📥 Download Resume as PDF",
        data=pdf_buffer,
        file_name=f"{name}_Resume.pdf",
        mime="application/pdf"
    )

    if st.button("🔄 Regenerate Resume"):
        st.session_state.resume_generated = False
