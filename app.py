import streamlit as st
import io
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

            pdf.multi_cell(190  , 5, text=f"{exp['summary']}")
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
            #pdf.cell(200, 5, text=f"Links: {project['links']}", ln=True)
            pdf.ln(2)
        pdf.ln(2)
    
    # Add skills
    if len(details['technical_skills'][0])>0 or len(details['languages'][0])>0 or len(details['frameworks_libraries'][0])>0     :
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, text="Skills", ln=True, align='L')
        
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        if len(details['technical_skills'][0])>0:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(30, 5, text="Technical Skills: ",ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=", ".join(details['technical_skills']).strip())

        if len(details['languages'][0])>0:
            pdf.ln(1)
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(22, 5, text="Languages: ", ln=False, align='L')
            pdf.set_font("Arial", size=10.5)
            pdf.multi_cell(0, 5, text=", ".join(details['languages']).strip())
        
        if len(details['frameworks_libraries'][0])>0:
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
            pdf.set_font("Arial", size=10.5 )
            pdf.cell(95, 5, text=f"{cert['date']}", ln=True, align='R')
            #pdf.cell(200, 5, text=f"Link: {cert['link']}", ln=True)
            pdf.multi_cell(0, 5, text=cert['description'],ln=True)
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
            pdf.cell(200, 5, text=f"{add['title']}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(200, 5, text={add['date']}, ln=True, align='R')
            pdf.multi_cell(0, 10, text=add['summary'], ln=True)
    
    # Add coding platforms
    if details['codechef'] or details['leetcode'] or details['hackerrank'] or details['codeforces']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, text="Coding Platforms", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        if details['codechef']:
            pdf.cell(200, 10, text=f"CodeChef: {details['codechef']}", ln=True)
        if details['leetcode']:
            pdf.cell(200, 10, text=f"LeetCode: {details['leetcode']}", ln=True)
        if details['hackerrank']:
            pdf.cell(200, 10, text=f"HackerRank: {details['hackerrank']}", ln=True)
        if details['codeforces']:
            pdf.cell(200, 10, text=f"Codeforces: {details['codeforces']}", ln=True)
    
    
    return pdf

# Function to display the PDF in Streamlit
def display_pdf(pdf):
    #encode the buffer contenet using base64
    buffer = io.BytesIO()
    pdf.output(buffer,"F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

#function to download the pdf
def download_pdf(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer,"F")
    buffer.seek(0)
    base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    st.markdown(f'<a href="data:application/pdf;base64,{base64_pdf}" download="resume.pdf">Click here to download</a>', unsafe_allow_html=True)


# Default details for demonstration
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
    # Personal Information Section
    with st.expander("Personal Information"):
        details["name"] = st.text_input("Name")
        details["email"] = st.text_input("Email")
        details["phone"] = st.text_input("Phone")
        details["address"] = st.text_area("Address")

    # Education Section
    with st.expander("Education"):
        if "education" not in st.session_state:
            st.session_state.education = []
        num_edu = st.number_input("Number of education entries", min_value=0, value=len(st.session_state.education))
        st.session_state.education = st.session_state.education[:num_edu]  # Adjust length
        for i in range(num_edu):
            if len(st.session_state.education) <= i:
                st.session_state.education.append({})
            with st.container():
                st.session_state.education[i]['institution'] = st.text_input(f"Institution {i+1}", key=f'institution_{i}')
                st.session_state.education[i]['location'] = st.text_input(f"Location {i+1}", key=f'location_{i}')
                st.session_state.education[i]['degree'] = st.text_input(f"Degree {i+1}", key=f'degree_{i}')
                st.session_state.education[i]['year_in'] = st.text_input(f"Start Year {i+1}", key=f'year_in_{i}')
                st.session_state.education[i]['year_out'] = st.text_input(f"End Year {i+1}", key=f'year_out_{i}')
                st.session_state.education[i]['gpa'] = st.text_input(f"GPA {i+1}", key=f'gpa_{i}')
        details['education'] = st.session_state.education

    # Experience Section
    with st.expander("Experience"):
        if "experience" not in st.session_state:
            st.session_state.experience = []
        num_exp = st.number_input("Number of experience entries", min_value=0, value=len(st.session_state.experience))
        st.session_state.experience = st.session_state.experience[:num_exp]  # Adjust length
        for i in range(num_exp):
            if len(st.session_state.experience) <= i:
                st.session_state.experience.append({})
            with st.container():
                st.session_state.experience[i]['company'] = st.text_input(f"Company {i+1}", key=f'company_{i}')
                st.session_state.experience[i]['location'] = st.text_input(f"Location {i+1}", key=f'location_exp_{i}')
                st.session_state.experience[i]['role'] = st.text_input(f"Role {i+1}", key=f'role_{i}')
                st.session_state.experience[i]['year_in'] = st.text_input(f"Start Year {i+1}", key=f'year_in_exp_{i}')
                st.session_state.experience[i]['year_out'] = st.text_input(f"End Year {i+1}", key=f'year_out_exp_{i}')
                st.session_state.experience[i]['summary'] = st.text_area(f"Summary {i+1}", key=f'summary_{i}')
        details['experience'] = st.session_state.experience

    # Projects Section
    with st.expander("Projects"):
        if "projects" not in st.session_state:
            st.session_state.projects = []
        num_proj = st.number_input("Number of projects", min_value=0, value=len(st.session_state.projects))
        st.session_state.projects = st.session_state.projects[:num_proj]  # Adjust length
        for i in range(num_proj):
            if len(st.session_state.projects) <= i:
                st.session_state.projects.append({})
            with st.container():
                st.session_state.projects[i]['title'] = st.text_input(f"Project Title {i+1}", key=f'title_proj_{i}')
                st.session_state.projects[i]['date'] = st.text_input(f"Project Date {i+1}", key=f'date_proj_{i}')
                st.session_state.projects[i]['summary'] = st.text_area(f"Project Summary {i+1}", key=f'summary_proj_{i}')
                st.session_state.projects[i]['links'] = st.text_input(f"Project Links {i+1}", key=f'links_proj_{i}')
        details['projects'] = st.session_state.projects

    # Skills Section
    with st.expander("Skills"):
        details['technical_skills'] = st.text_area("Technical Skills (comma separated)").split(",")
        details['languages'] = st.text_area("Languages (comma separated)").split(",")
        details['frameworks_libraries'] = st.text_area("Frameworks/Libraries (comma separated)").split(",")

    # Certifications Section
    with st.expander("Certifications"):
        if "certifications" not in st.session_state:
            st.session_state.certifications = []
        num_cert = st.number_input("Number of certifications", min_value=0, value=len(st.session_state.certifications))
        st.session_state.certifications = st.session_state.certifications[:num_cert]  # Adjust length
        for i in range(num_cert):
            if len(st.session_state.certifications) <= i:
                st.session_state.certifications.append({})
            with st.container():
                st.session_state.certifications[i]['title'] = st.text_input(f"Certification Title {i+1}", key=f'title_cert_{i}')
                st.session_state.certifications[i]['provider'] = st.text_input(f"Provider {i+1}", key=f'provider_{i}')
                st.session_state.certifications[i]['date'] = st.text_input(f"Certification Date{i+1}", key=f"date_certi_{i}")
                st.session_state.certifications[i]['link'] = st.text_input(f"Certification Link {i+1}", key=f'link_cert_{i}')
                st.session_state.certifications[i]['description'] = st.text_area(f"Certification Description {i+1}", key=f'description_cert_{i}')
        details['certifications'] = st.session_state.certifications

    # Activities Section
    with st.expander("Activities"):
        if "activities" not in st.session_state:
            st.session_state.activities = []
        num_act = st.number_input("Number of activities", min_value=0, value=len(st.session_state.activities))
        st.session_state.activities = st.session_state.activities[:num_act]  # Adjust length
        for i in range(num_act):
            if len(st.session_state.activities) <= i:
                st.session_state.activities.append({})
            with st.container():
                st.session_state.activities[i]['title'] = st.text_input(f"Activity Title {i+1}", key=f'title_act_{i}')
                st.session_state.activities[i]['place'] = st.text_input(f"Activity Place {i+1}", key=f'place_act_{i}')
                st.session_state.activities[i]['year'] = st.text_input(f"Activity Year {i+1}", key=f'year_act_{i}')
                st.session_state.activities[i]['summary'] = st.text_area(f"Activity Summary {i+1}", key=f'summary_act_{i}')
        details['activities'] = st.session_state.activities

    # Additional Information Section
    with st.expander("Additional Information"):
        if "additional" not in st.session_state:
            st.session_state.additional = []
        num_add = st.number_input("Number of additional information entries", min_value=0, value=len(st.session_state.additional))
        st.session_state.additional = st.session_state.additional[:num_add]  # Adjust length
        for i in range(num_add):
            if len(st.session_state.additional) <= i:
                st.session_state.additional.append({})
            with st.container():
                st.session_state.additional[i]['title'] = st.text_input(f"Additional Info Title {i+1}", key=f'title_add_{i}')
                st.session_state.additional[i]['date'] = st.text_input(f"Date {i+1}", key=f'date_add_{i}')
                st.session_state.additional[i]['summary'] = st.text_area(f"Summary {i+1}", key=f'summary_add_{i}')
        details['additional'] = st.session_state.additional

    # Coding Platforms Section
    with st.expander("Coding Platforms"):
        details['codechef'] = st.text_input("CodeChef Username")
        details['leetcode'] = st.text_input("LeetCode Username")
        details['hackerrank'] = st.text_input("HackerRank Username")
        details['codeforces'] = st.text_input("Codeforces Username")

with right_col:
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Button to generate and display resume
    with col1:
        if st.button("Generate Resume"):
            pdf = generate_pdf(details)
            display_pdf(pdf)
    
    # Button to download resume
    with col2:
        if st.button("Download Resume"):
            pdf = generate_pdf(details)
            download_pdf(pdf)

