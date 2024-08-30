import streamlit as st
import io
from fpdf import FPDF
import base64
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")


def generate_pdf(details):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16, style='B')
    if details['name'] == "":
        details['name'] = "Your Name"
    pdf.cell(200, 5, text=details['name'].upper(), ln=True, align='C')

    pdf.set_font("Arial", size=10.5)
    if details['address'] == "":
        details['address'] = "Your Address"
    if details['phone'] == "":
        details['phone'] = "Your Phone"
    if details['email'] == "":
        details['email'] = "Your Email"
    personal_details = f"{details['address']} | {details['phone']} | {details['email']}"
    pdf.cell(200, 5, text=personal_details, ln=True, align='C')

    # Education
    if details['education']:
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(200, 5, text="EDUCATION", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for edu in details['education']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, text=f"{edu['institution'].upper()}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{edu['location']}", ln=True, align='R')

            pdf.cell(95, 5, text=f"{edu['degree']}", ln=False)
            pdf.cell(95, 5, text=f"{edu['year_in']} - {edu['year_out']}", ln=True, align='R')

            pdf.cell(200, 5, text=f"Cumulative GPA: {edu['gpa']}", ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # Add experience details
    if details['experience']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Experience", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for exp in details['experience']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, text=f"{exp['company'].upper()}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{exp['location']}", ln=True, align='R')

            pdf.cell(95, 5, text=f"{exp['role']}", ln=False)
            pdf.cell(95, 5, text=f"{exp['year_in']} - {exp['year_out']}", ln=True, align='R')

            pdf.multi_cell(190, 5, text=f"{exp['summary']}")
            pdf.ln(2)
        pdf.ln(2)

    # Add projects
    if details['projects']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Projects", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for project in details['projects']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, text=f"{project['title'].upper()}", ln=False, link=f"{project['links']}")

            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{project['date']}", ln=True, align='R')

            pdf.multi_cell(190, 5, text=f"{project['summary']}", ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # Add skills
    if len(details['technical_skills'][0]) > 0 or len(details['languages'][0]) > 0 or len(details['frameworks_libraries'][0]) > 0:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Skills", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        if len(details['technical_skills'][0]) > 0:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(30, 5, text="Technical Skills: ", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=", ".join(details['technical_skills']).strip())

        if len(details['languages'][0]) > 0:
            pdf.ln(1)
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(22, 5, text="Languages: ", ln=False, align='L')
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=", ".join(details['languages']).strip())

        if len(details['frameworks_libraries'][0]) > 0:
            pdf.ln(1)
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(40, 5, text="Frameworks/Libraries: ", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=", ".join(details['frameworks_libraries']).strip())

        pdf.ln(2)

    return pdf


def display_pdf(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def download_pdf(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    st.markdown(f'<a href="data:application/pdf;base64,{base64_pdf}" download="resume.pdf">Click here to download</a>',
                unsafe_allow_html=True)


details = {
    "name": "",
    "email": "",
    "phone": "",
    "address": "",
    "education": [],
    "experience": [],
    "projects": [],
    "technical_skills": [],
    "languages": [],
    "frameworks_libraries": [],
    "certifications": [],
    "activities": [],
    "additional": [],
    "codechef": "",
    "leetcode": "",
    "hackerrank": "",
    "codeforces": ""
}

st.title("Resume Generator")
left_col, right_col = st.columns(2)

with left_col:
    details["name"] = st.text_input("Name")
    details["email"] = st.text_input("Email")
    details["phone"] = st.text_input("Phone")
    details["address"] = st.text_area("Address")

    # Education Section
    num_edu = st.number_input("Number of education entries", min_value=0, value=0)
    for i in range(num_edu):
        with st.container():
            institution = st.text_input(f"Institution {i + 1}")
            location = st.text_input(f"Location {i + 1}")
            degree = st.text_input(f"Degree {i + 1}")
            year_in = st.text_input(f"Start Year {i + 1}")
            year_out = st.text_input(f"End Year {i + 1}")
            gpa = st.text_input(f"GPA {i + 1}")
            details['education'].append({
                'institution': institution, 'location': location, 'degree': degree,
                'year_in': year_in, 'year_out': year_out, 'gpa': gpa
            })

    # Experience Section
    num_exp = st.number_input("Number of experience entries", min_value=0, value=0)
    for i in range(num_exp):
        with st.container():
            company = st.text_input(f"Company {i + 1}")
            location = st.text_input(f"Location {i + 1}")
            role = st.text_input(f"Role {i + 1}")
            year_in = st.text_input(f"Start Year {i + 1}")
            year_out = st.text_input(f"End Year {i + 1}")
            summary = st.text_area(f"Summary {i + 1}")
            details['experience'].append({
                'company': company, 'location': location, 'role': role,
                'year_in': year_in, 'year_out': year_out, 'summary': summary
            })

with right_col:
    # Projects Section
    num_projects = st.number_input("Number of projects entries", min_value=0, value=0)
    for i in range(num_projects):
        with st.container():
            title = st.text_input(f"Project Title {i + 1}")
            links = st.text_input(f"Project Link {i + 1}")
            date = st.text_input(f"Project Date {i + 1}")
            summary = st.text_area(f"Project Summary {i + 1}")
            details['projects'].append({
                'title': title, 'links': links, 'date': date, 'summary': summary
            })

    # Skills Section
    technical_skills = st.text_area("Technical Skills (comma separated)").split(',')
    languages = st.text_area("Languages (comma separated)").split(',')
    frameworks_libraries = st.text_area("Frameworks/Libraries (comma separated)").split(',')

    details["technical_skills"] = technical_skills
    details["languages"] = languages
    details["frameworks_libraries"] = frameworks_libraries

if st.button("Generate Resume"):
    pdf = generate_pdf(details)
    display_pdf(pdf)
    download_pdf(pdf)
