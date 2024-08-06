import io
import base64
from fpdf import FPDF
import streamlit as st

# Assuming you have a function to generate the PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Hello World", ln=True, align='C')

# Create an in-memory bytes buffer
buffer = io.BytesIO()
pdf.output(buffer, "F")
buffer.seek(0)

# Encode the buffer content to base64
base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')

# Display the PDF using the base64 encoded string
pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="600" type="application/pdf">'
st.markdown(pdf_display, unsafe_allow_html=True)

# Add a download button
download_button = st.button("Download PDF")

if download_button:
    # Set the appropriate headers for a PDF file
    st.header("Download PDF")
    st.markdown(f'<a href="data:application/pdf;base64,{base64_pdf}" download="resume.pdf">Click here to download</a>', unsafe_allow_html=True)