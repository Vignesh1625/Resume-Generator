import streamlit as st
from fpdf import FPDF
import base64
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

# Function to generate PDF
def generate_pdf(details):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the title
    pdf.set_font("Arial", size=16, style='B')
    
    # If name is null, make it "Your Name"
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

    # Add certifications
    if details['certifications']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Certifications", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for cert in details['certifications']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, text=f"{cert['title'].upper()}", ln=False, link=f"{cert['link']}")
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, text=f"{cert['date']}", ln=True, align='R')
            pdf.multi_cell(0, 5, text=cert['description'], ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # Add activities
    if details['activities']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Activities", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for act in details['activities']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, text=f"{act['title'].upper()}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(200, 5, text=f"{act['place']} , {act['year']}", ln=True, align='R')
            pdf.multi_cell(0, 5, text=act['summary'])
            pdf.ln(2)
        pdf.ln(2)   
    
    # Add additional information
    if details['additional']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Additional Information", ln=True, align='L')

        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for add in details['additional']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(200, 5, text=f"{add['title'].upper()}", ln=True)
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=add['summary'])
            pdf.ln(2)
        pdf.ln(2)

    return pdf

# Function to save PDF to file
def save_pdf(pdf, filename):
    pdf.output(filename)

# Function to download link
def get_pdf_download_link(pdf, filename):
    save_pdf(pdf, filename)
    with open(filename, "rb") as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Resume</a>'
    return href

# Sidebar for input
st.sidebar.title("Resume Generator")
details = {
    "name": st.sidebar.text_input("Name"),
    "address": st.sidebar.text_input("Address"),
    "phone": st.sidebar.text_input("Phone"),
    "email": st.sidebar.text_input("Email"),
    "education": [],
    "experience": [],
    "projects": [],
    "technical_skills": [st.sidebar.text_area("Technical Skills").split(",")],
    "languages": [st.sidebar.text_area("Languages").split(",")],
    "frameworks_libraries": [st.sidebar.text_area("Frameworks/Libraries").split(",")],
    "certifications": [],
    "activities": [],
    "additional": [],
}

# Education section
st.sidebar.subheader("Education")
institution = st.sidebar.text_input("Institution")
location = st.sidebar.text_input("Location")
degree = st.sidebar.text_input("Degree")
year_in = st.sidebar.text_input("Year In")
year_out = st.sidebar.text_input("Year Out")
gpa = st.sidebar.text_input("Cumulative GPA")
if st.sidebar.button("Add Education"):
    details["education"].append({
        "institution": institution,
        "location": location,
        "degree": degree,
        "year_in": year_in,
        "year_out": year_out,
        "gpa": gpa,
    })

# Experience section
st.sidebar.subheader("Experience")
company = st.sidebar.text_input("Company")
location = st.sidebar.text_input("Location", key="exp_location")
role = st.sidebar.text_input("Role")
year_in = st.sidebar.text_input("Year In", key="exp_year_in")
year_out = st.sidebar.text_input("Year Out", key="exp_year_out")
summary = st.sidebar.text_area("Summary")
if st.sidebar.button("Add Experience"):
    details["experience"].append({
        "company": company,
        "location": location,
        "role": role,
        "year_in": year_in,
        "year_out": year_out,
        "summary": summary,
    })

# Projects section
st.sidebar.subheader("Projects")
title = st.sidebar.text_input("Project Title")
links = st.sidebar.text_input("Links")
date = st.sidebar.text_input("Date")
summary = st.sidebar.text_area("Project Summary")
if st.sidebar.button("Add Project"):
    details["projects"].append({
        "title": title,
        "links": links,
        "date": date,
        "summary": summary,
    })

# Certifications section
st.sidebar.subheader("Certifications")
title = st.sidebar.text_input("Certification Title")
link = st.sidebar.text_input("Link")
date = st.sidebar.text_input("Date", key="cert_date")
description = st.sidebar.text_area("Description")
if st.sidebar.button("Add Certification"):
    details["certifications"].append({
        "title": title,
        "link": link,
        "date": date,
        "description": description,
    })

# Activities section
st.sidebar.subheader("Activities")
title = st.sidebar.text_input("Activity Title")
place = st.sidebar.text_input("Place")
year = st.sidebar.text_input("Year")
summary = st.sidebar.text_area("Activity Summary")
if st.sidebar.button("Add Activity"):
    details["activities"].append({
        "title": title,
        "place": place,
        "year": year,
        "summary": summary,
    })

# Additional information section
st.sidebar.subheader("Additional Information")
title = st.sidebar.text_input("Additional Title")
summary = st.sidebar.text_area("Additional Summary")
if st.sidebar.button("Add Additional Information"):
    details["additional"].append({
        "title": title,
        "summary": summary,
    })

# Main section
st.title("Resume Preview")

generate_clicked = st.button("Generate Resume")
if generate_clicked:
    pdf = generate_pdf(details)
    st.markdown("## Resume Generated!")
    st.markdown(get_pdf_download_link(pdf, "resume.pdf"), unsafe_allow_html=True)
    
if 'pdf' in locals() and not generate_clicked:
    st.markdown(get_pdf_download_link(pdf, "resume.pdf"), unsafe_allow_html=True)
    st.markdown("## Resume Preview (Click Generate to Update)")
