import streamlit as st
from fpdf import FPDF
import base64

# Function to generate PDF
def generate_pdf(details):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the title
    pdf.set_font("Arial", size=16, style='B')
    
    # If name is null, make it "Your Name"
    if details['name'] == "":
        details['name'] = "Your Name"
    pdf.cell(200, 5, txt=details['name'].upper(), ln=True, align='C')

    pdf.set_font("Arial", size=10.5)
    if details['address'] == "":
        details['address'] = "Your Address"
    if details['phone'] == "":
        details['phone'] = "Your Phone"
    if details['email'] == "":
        details['email'] = "Your Email"
    personal_details = f"{details['address']} | {details['phone']} | {details['email']}"
    pdf.cell(200, 5, txt=personal_details, ln=True, align='C')

    # Education
    if details['education']:
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(200, 5, txt="EDUCATION", ln=True, align='L')
        
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)  

        for edu in details['education']:
            pdf.set_font("Arial", size=10.5, style='B')
            pdf.cell(95, 5, txt=f"{edu['institution']}", ln=False)
            pdf.set_font("Arial", size=10.5)
            pdf.cell(95, 5, txt=f"{edu['location']}", ln=True, align='R')

            pdf.cell(95, 5, txt=f"{edu['degree']}", ln=False)
            pdf.cell(95, 5, txt=f"{edu['year_in']} - {edu['year_out']}", ln=True, align='R')

            pdf.cell(200, 5, txt=f"Cumulative GPA: {edu['gpa']}", ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # Add experience details
    if details['experience']:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.cell(200, 5, txt="Experience", ln=True, align='L')
        
        y_position = pdf.get_y()
        pdf.set_line_width(0.3)
        pdf.line(10, y_position, 200, y_position)
        pdf.ln(1)

        for exp in details['experience']:
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(95, 10, txt=f"{exp['company']}", ln=False)
            pdf.set_font("Arial", size=12)
            pdf.cell(95, 10, txt=f"{exp['location']}", ln=True, align='R')

            pdf.cell(95, 10, txt=f"{exp['role']}", ln=False)
            pdf.cell(95, 10, txt=f"{exp['year_in']} - {exp['year_out']}", ln=True, align='R')

            pdf.multi_cell(0, 10, txt=f"• {exp['summary']}")
            pdf.ln(2)
        pdf.ln(2)
    
    # Add projects
    if details['projects']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Projects", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        for project in details['projects']:
            pdf.cell(200, 10, txt=f"Title: {project['title']} ({project['date']})", ln=True)
            pdf.multi_cell(0, 10, txt=f"Summary: {project['summary']}")
            pdf.cell(200, 10, txt=f"Links: {project['links']}", ln=True)
    

    # Add skills
    print(details['technical_skills'], details['languages'], details['frameworks_libraries'])
    print(len(details['technical_skills'][0]), len(details['languages'][0]), len(details['frameworks_libraries'][0]))
    
    if len(details['technical_skills'][0])>0 or len(details['languages'][0])>0 or len(details['frameworks_libraries'][0])>0:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Skills", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        
        if len(details['technical_skills'][0])>0:
            pdf.cell(200, 10, txt="Technical Skills: ", ln=True)
            pdf.cell(200, 10, txt=", ".join(details['technical_skills'][0]).strip(), ln=True)
        
        if len(details['languages'][0])>0:
            pdf.cell(200, 10, txt="Languages: ", ln=True)
            pdf.cell(200, 10, txt=", ".join(details['languages'][0]).strip(), ln=True)
        
        if len(details['frameworks_libraries'][0])>0:
            pdf.cell(200, 10, txt="Frameworks/Libraries: ", ln=True)
            pdf.cell(200, 10, txt=", ".join(details['frameworks_libraries'][0]).strip(), ln=True)

    # Add certifications
    if details['certifications']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Certifications", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        for cert in details['certifications']:
            pdf.cell(200, 10, txt=f"{cert['title']} by {cert['provider']}", ln=True)
            pdf.cell(200, 10, txt=f"ID: {cert['id']}, Link: {cert['link']}", ln=True)
            pdf.multi_cell(0, 10, txt=cert['description'])
    
    # Add activities
    if details['activities']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Activities", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        for act in details['activities']:
            pdf.cell(200, 10, txt=f"{act['title']} at {act['place']} ({act['year']})", ln=True)
            pdf.multi_cell(0, 10, txt=act['summary'])
    
    # Add additional information
    if details['additional']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Additional Information", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        for add in details['additional']:
            pdf.cell(200, 10, txt=f"{add['title']} ({add['date']})", ln=True)
            pdf.multi_cell(0, 10, txt=add['summary'])
    
    # Add coding platforms
    if details['codechef'] or details['leetcode'] or details['hackerrank'] or details['codeforces']:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Coding Platforms", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        if details['codechef']:
            pdf.cell(200, 10, txt=f"CodeChef: {details['codechef']}", ln=True)
        if details['leetcode']:
            pdf.cell(200, 10, txt=f"LeetCode: {details['leetcode']}", ln=True)
        if details['hackerrank']:
            pdf.cell(200, 10, txt=f"HackerRank: {details['hackerrank']}", ln=True)
        if details['codeforces']:
            pdf.cell(200, 10, txt=f"Codeforces: {details['codeforces']}", ln=True)
    
    # Save the PDF
    pdf_output = f"resume_{details['name'].replace(' ', '_')}.pdf"
    pdf.output(pdf_output.encode('latin1'))
    return pdf_output

# Function to display the PDF in Streamlit
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

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

# Page layout configuration
st.set_page_config(layout="wide")
left_col, right_col = st.columns([2, 2])

with left_col:
    st.header("Enter Your Details")
    
    details = {}
    details['name'] = st.text_input("Name")
    details['email'] = st.text_input("Email")
    details['phone'] = st.text_input("Phone")
    details['address'] = st.text_input("Address")
    
    st.subheader("Education")
    education_count = st.number_input("Number of educational qualifications", min_value=0, max_value=10, step=1)
    details['education'] = []
    for i in range(int(education_count)):
        st.write(f"### Education {i+1}")
        institution = st.text_input(f"Institution {i+1}", key=f"institution_{i}")
        location = st.text_input(f"Location {i+1}", key=f"location_{i}")
        degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
        year_in = st.text_input(f"Year In {i+1}", key=f"year_in_{i}")
        year_out = st.text_input(f"Year Out {i+1}", key=f"year_out_{i}")
        gpa = st.text_input(f"GPA {i+1}", key=f"gpa_{i}")
        details['education'].append({"institution": institution, "location": location, "degree": degree, "year_in": year_in, "year_out": year_out, "gpa": gpa})
    
    st.subheader("Experience")
    experience_count = st.number_input("Number of job experiences", min_value=0, max_value=10, step=1)
    details['experience'] = []
    for i in range(int(experience_count)):
        st.write(f"### Experience {i+1}")
        company = st.text_input(f"Company {i+1}", key=f"company_{i}")
        location = st.text_input(f"Location {i+1}", key=f"exp_location_{i}")
        role = st.text_input(f"Role {i+1}", key=f"exp_role_{i}")
        year_in = st.text_input(f"Year In {i+1}", key=f"exp_year_in_{i}")
        year_out = st.text_input(f"Year Out {i+1}", key=f"exp_year_out_{i}")
        summary = st.text_area(f"Summary {i+1}", key=f"exp_summary_{i}")
        details['experience'].append({"company": company, "location": location, "role": role, "year_in": year_in, "year_out": year_out, "summary": summary})
    
    st.subheader("Projects")
    projects_count = st.number_input("Number of projects", min_value=0, max_value=10, step=1)
    details['projects'] = []
    for i in range(int(projects_count)):
        st.write(f"### Project {i+1}")
        title = st.text_input(f"Title {i+1}", key=f"project_title_{i}")
        date = st.text_input(f"Date {i+1}", key=f"project_date_{i}")
        summary = st.text_area(f"Summary/Points {i+1}", key=f"project_summary_{i}")
        links = st.text_input(f"Links {i+1}", key=f"project_links_{i}")
        details['projects'].append({"title": title, "date": date, "summary": summary, "links": links})
    
    st.subheader("Skills")
    details['technical_skills'] = st.text_area("Technical Skills (comma-separated)").split(',')
    details['languages'] = st.text_area("Languages (comma-separated)").split(',')
    details['frameworks_libraries'] = st.text_area("Frameworks/Libraries (comma-separated)").split(',')
    
    st.subheader("Certifications")
    certifications_count = st.number_input("Number of certifications", min_value=0, max_value=10, step=1)
    details['certifications'] = []
    for i in range(int(certifications_count)):
        st.write(f"### Certification {i+1}")
        title = st.text_input(f"Certification Title {i+1}", key=f"cert_title_{i}")
        provider = st.text_input(f"Provider {i+1}", key=f"cert_provider_{i}")
        cert_id = st.text_input(f"ID {i+1}", key=f"cert_id_{i}")
        link = st.text_input(f"Link {i+1}", key=f"cert_link_{i}")
        description = st.text_area(f"Description {i+1}", key=f"cert_description_{i}")
        details['certifications'].append({"title": title, "provider": provider, "id": cert_id, "link": link, "description": description})
    
    st.subheader("Activities")
    activities_count = st.number_input("Number of activities", min_value=0, max_value=10, step=1)
    details['activities'] = []
    for i in range(int(activities_count)):
        st.write(f"### Activity {i+1}")
        title = st.text_input(f"Activity Title {i+1}", key=f"act_title_{i}")
        place = st.text_input(f"Place {i+1}", key=f"act_place_{i}")
        year = st.text_input(f"Year {i+1}", key=f"act_year_{i}")
        summary = st.text_area(f"Summary {i+1}", key=f"act_summary_{i}")
        details['activities'].append({"title": title, "place": place, "year": year, "summary": summary})
    
    st.subheader("Additional Information")
    additional_count = st.number_input("Number of additional info items", min_value=0, max_value=10, step=1)
    details['additional'] = []
    for i in range(int(additional_count)):
        st.write(f"### Additional Info {i+1}")
        title = st.text_input(f"Additional Title {i+1}", key=f"add_title_{i}")
        date = st.text_input(f"Date {i+1}", key=f"add_date_{i}")
        summary = st.text_area(f"Summary {i+1}", key=f"add_summary_{i}")
        details['additional'].append({"title": title, "date": date, "summary": summary})
    
    st.subheader("Coding Platforms")
    details['codechef'] = st.text_input("CodeChef Username")
    details['leetcode'] = st.text_input("LeetCode Username")
    details['hackerrank'] = st.text_input("HackerRank Username")
    details['codeforces'] = st.text_input("Codeforces Username")

    if st.button("Generate Resume"):
        pdf_file = generate_pdf(details)
        st.success("Resume generated successfully!")

with right_col:
    st.header("Resume Preview")
    if "pdf_file" in locals():
        display_pdf(pdf_file)
    else:
        st.write("Your resume preview will appear here after generation.")
