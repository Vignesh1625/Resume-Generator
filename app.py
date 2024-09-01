import streamlit as st
import io
from fpdf import FPDF
import base64
import warnings
import os
import google.generativeai as genai


warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

API_KEY = "AIzaSyAe0jHn8sIEmTMpbE5X9CMqvyG5h4cgMfM"
os.environ["API_KEY"] = API_KEY
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
def repharseSentence(sentence):
    query = "Convert this Sentense Into a Professional Format by Adding required things to it in just 30 words"
    sendedInfo = query+sentence
    repharsed = model.generate_content(sendedInfo)
    return repharsed

def generate_pdf(details):
    pdf = FPDF()
    pdf.add_page()

    # Name and personal details
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 5, text=details['name'].upper(), ln=True, align='C')
    pdf.set_font("Arial", size=10.5)
    personal_details = f"{details['address']} | {details['phone']} | {details['email']}"
    pdf.cell(200, 5, text=personal_details, ln=True, align='C')

    # Education Section
    if details['education']:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="EDUCATION", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for edu in details['education']:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(95, 5, text=f"{edu['institution'].upper()}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{edu['location']}", ln=True, align='R')

            pdf.set_font("Arial", size=9)  # Smaller sub-detail
            pdf.cell(95, 5, text=f"{edu['degree']}", ln=False)
            pdf.cell(95, 5, text=f"{edu['year_in']} - {edu['year_out']}", ln=True, align='R')

            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.cell(200, 5, text=f"Cumulative GPA: {edu['gpa']}", ln=True)
            pdf.ln(0.5)
        pdf.ln(1)

    # Experience Section
    if details['experience']:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="WORK EXPERIENCE", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for exp in details['experience']:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(95, 5, text=f"{exp['company'].upper()}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{exp['location']}", ln=True, align='R')

            pdf.set_font("Arial", size=9)  # Smaller sub-detail
            pdf.cell(95, 5, text=f"{exp['role']}", ln=False)
            pdf.cell(95, 5, text=f"{exp['year_in']} - {exp['year_out']}", ln=True, align='R')

            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(190, 5, text=repharseSentence(exp['summary']))
            pdf.ln(2)
        pdf.ln(2)

    # Projects Section
    if details['projects']:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="PROJECTS", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for project in details['projects']:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(95, 5, text=f"{project['title'].upper()}", ln=False, link=f"{project['links']}")

            pdf.set_font("Arial", size=9)  # Smaller sub-detail
            pdf.cell(95, 5, text=f"{project['date']}", ln=True, align='R')

            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(190, 5, text=repharseSentence(project['summary']), ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # Certifications Section
    if details['certifications']:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="CERTIFICATIONS", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for cert in details['certifications']:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(95, 5, text=f"{cert['certification'].upper()}", ln=False)
            pdf.set_font("Arial", size=9)  # Smaller sub-detail
            pdf.cell(95, 5, text=f"{cert['date']}", ln=True, align='R')

            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(190, 5, text=repharseSentence(cert['summary']))
            pdf.ln(2)
        pdf.ln(2)
    
    # Activities Section
    if details['activities']:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="ACTIVITIES", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for activity in details['activities']:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(95, 5, text=f"{activity['activity'].upper()}", ln=False)
            pdf.set_font("Arial", size=9)  # Smaller sub-detail
            pdf.cell(95, 5, text=f"{activity['date']}", ln=True, align='R')

            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(190, 5, text=repharseSentence(activity['summary']))
            pdf.ln(2)
        pdf.ln(2)
        
    # Skills Section
    if len(details['technical_skills'][0]) > 0 or len(details['languages'][0]) > 0 or len(details['frameworks_libraries'][0]) > 0:
        pdf.set_font("Arial", size=11, style='B')  # Main section heading
        pdf.cell(200, 5, text="SKILLS", ln=True, align='L')
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        if len(details['technical_skills'][0]) > 0:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(30, 5, text="Technical Skills: ", ln=False)
            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(0, 5, text=", ".join(details['technical_skills']).strip())

        if len(details['languages'][0]) > 0:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(22, 5, text="Languages: ", ln=False, align='L')
            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(0, 5, text=", ".join(details['languages']).strip())

        if len(details['frameworks_libraries'][0]) > 0:
            pdf.set_font("Arial", size=10.5, style='B')  # Subheading
            pdf.cell(40, 5, text="Frameworks/Libraries: ", ln=False)
            pdf.set_font("Arial", size=10)  # Paragraph text
            pdf.multi_cell(0, 5, text=", ".join(details['frameworks_libraries']).strip())

        pdf.ln(2)

    return pdf


def display_pdf(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1000" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def download_pdf(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    st.markdown(f'<a href="data:application/pdf;base64,{base64_pdf}" download="resume.pdf">Click here to download</a>',
                unsafe_allow_html=True)
details = {
    "personal_details": {},
    "education": [],
    "experience": [],
    "certifications": [],
    "activities": [],
    "projects": [],
    "technical_skills": [],
    "languages": [],
    "frameworks_libraries": []
}

st.title("Resume Generator")
left_col, right_col = st.columns(2)

with left_col:
    with st.expander("Personal Details"):
        details["name"] = st.text_input("Name", value="", key="personal_name")
        left ,right = st.columns(2)
        with left:
            details["email"] = st.text_input("Email", value="", key="personal_email")
        with right:
            details["phone"] = st.text_input("Phone", value="", key="personal_phone")
        details["address"] = st.text_input("Address", key="personal_address")

    # Education Section
    with st.expander("Education"):
        num_edu = st.number_input("Number of education entries", min_value=0, value=0, key="num_edu")
        for i in range(num_edu):
            with st.container():
                institution = st.text_input(f"Institution {i + 1}", key=f"edu_institution_{i+1}")
                left ,right = st.columns(2)
                with left:
                    degree = st.text_input(f"Degree {i + 1}", key=f"edu_degree_{i+1}")
                    year_in = st.date_input(f"Start Year {i + 1}", value=None, key=f"edu_start_{i+1}")
                with right:
                    location = st.text_input(f"Location {i + 1}", key=f"edu_location_{i+1}")
                    year_out = st.date_input(f"End Year {i + 1}", value=None, key=f"edu_end_{i+1}")

                gpa = st.text_input(f"GPA {i + 1}", key=f"edu_gpa_{i+2}")
                details['education'].append({
                    'institution': institution, 'location': location, 'degree': degree,
                    'year_in': year_in, 'year_out': year_out, 'gpa': gpa
                })

    # Experience Section
    with st.expander("Experience"):
        num_exp = st.number_input("Number of experience entries", min_value=0, value=0, key="num_exp")
        for i in range(num_exp):
            with st.container():
                company = st.text_input(f"Company {i + 1}", key=f"exp_company_{i+1}")
                left, right  = st.columns(2)
                with left:
                    exp_role = st.text_input(f"Role {i + 1}", key=f"exp_role_{i}")
                    exp_year_in = st.date_input(f"Start Year {i + 1}", value=None, key=f"exp_start_{i+1}")
                with right:
                    exp_location = st.text_input(f"Location {i + 1}", key=f"exp_location_{i+1}")
                    exp_year_out = st.date_input(f"End Year {i + 1}", value=None, key=f"exp_end_{i+1}")
                exp_summary = st.text_area(f"Summary {i + 1}", key=f"exp_summary_{i+1}")
                details['experience'].append({
                    'company': company, 'location': exp_location, 'role': exp_role,
                    'year_in': exp_year_in, 'year_out': exp_year_out, 'summary': exp_summary
                })

    # Certifications Section
    with st.expander("Certifications"):
        num_certifications = st.number_input("Number of certifications entries", min_value=0, value=0, key="num_certifications")
        for i in range(num_certifications):
            with st.container():
                left, right = st.columns([5,2])
                with left:
                    certification = st.text_input(f"Certification {i + 1}", key=f"cert_name_{i+1}")
                with right:
                    date = st.date_input(f"Date {i + 1}", value=None, key=f"cert_date_{i+1}")
                summary = st.text_area(f"Summary {i + 1}", key=f"cert_summary_{i+1}")
                details['certifications'].append({
                    'certification': certification, 'date': date, 'summary': summary
                })

with right_col:
     # Activities Section
    with st.expander("Activities"):
        num_activities = st.number_input("Number of Activities entries", min_value=0, value=0, key="num_activities")
        for i in range(num_activities):
            with st.container():
                left, right = st.columns([5,2])
                with left:
                    activity = st.text_input(f"Activity {i + 1}", key=f"activity_{i+1}")
                with right:
                    date = st.date_input(f"Date {i + 1}", value=None, key=f"activity_date_{i+1}")
                summary = st.text_area(f"Summary {i + 1}", key=f"activity_summary_{i+1}")
                details['activities'].append({
                    'activity': activity, 'date': date, 'summary': summary
                })

    # Projects Section
    with st.expander("Projects"):
        num_projects = st.number_input("Number of projects entries", min_value=0, value=0, key="num_projects")
        for i in range(num_projects):
            with st.container():
                title = st.text_input(f"Project Title {i + 1}", key=f"proj_title_{i+1}")
                left, right = st.columns(2)
                with left:
                    links = st.text_input(f"Project Link {i + 1}", key=f"proj_link_{i+1}")
                with right:
                    date = st.date_input(f"Project Date {i + 1}", value=None, key=f"proj_date_{i+1}")
                summary = st.text_area(f"Project Summary {i + 1}", key=f"proj_summary_{i+1}")
                details['projects'].append({
                    'title': title, 'links': links, 'date': date, 'summary': summary
                })

    # Skills Section
    with st.expander("Skills"):
        technical_skills = st.text_area("Technical Skills (comma separated)", key="skills_technical").split(',')
        languages = st.text_area("Languages (comma separated)", key="skills_languages").split(',')
        frameworks_libraries = st.text_area("Frameworks/Libraries (comma separated)", key="skills_frameworks").split(',')

        details["technical_skills"] = technical_skills
        details["languages"] = languages
        details["frameworks_libraries"] = frameworks_libraries

if st.button("Generate Resume"):
    pdf = generate_pdf(details)
    display_pdf(pdf)
    download_pdf(pdf)
