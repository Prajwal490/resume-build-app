from jinja2 import Template
from xhtml2pdf import pisa
import streamlit as st
import os

# HTML Template
template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Helvetica', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            margin: 40px;
            color: #222;
        }

        h1 {
            font-size: 26px;
            color: #0b5394;
            margin-bottom: 5px;
        }

        h2 {
            font-size: 18px;
            border-bottom: 1px solid #ccc;
            margin-top: 30px;
            margin-bottom: 10px;
            color: #0b5394;
        }

        .section {
            margin-bottom: 20px;
        }

        .info {
            font-size: 14px;
            margin-bottom: 20px;
        }

        .info span {
            display: inline-block;
            margin-right: 15px;
        }

        ul {
            margin: 0;
            padding-left: 20px;
        }

        .job {
            margin-bottom: 10px;
        }

        .skills {
            margin-top: 10px;
        }

        .skills span {
            display: inline-block;
            background: #eee;
            padding: 4px 8px;
            margin: 4px;
            border-radius: 4px;
            font-size: 13px;
        }

        .summary {
            margin-top: 5px;
            font-style: italic;
        }

    </style>
</head>
<body>

    <h1>{{ name }}</h1>
    <div class="info">
        <span><strong>Email:</strong> {{ email }}</span>
        <span><strong>Phone:</strong> {{ phone }}</span>
    </div>

    <div class="section">
        <h2>Professional Summary</h2>
        <p class="summary">{{ summary }}</p>
    </div>

    <div class="section">
        <h2>Experience</h2>
        {% for job in experience %}
        <div class="job">
    <strong>{{ job.role }}</strong> at <strong>{{ job.company }}</strong><br>
    <small>Years at {{ job.company }}: {{ job.years }}</small>
</div>

        </div>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Skills</h2>
        <div class="skills">
            {% for skill in skills %}
            <span>{{ skill }}</span>
            {% endfor %}
        </div>
    </div>

</body>
</html>
"""


def convert_html_to_pdf(source_html, output_filename):
    with open(output_filename, "wb") as result_file:
        pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    return pisa_status.err

# Streamlit UI
st.title("Instant Resume Generator")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    summary = st.text_area("Professional Summary")
    company1 = st.text_input("Company 1")
    role1 = st.text_input("Role at Company 1")
    years1 = st.text_input("Years at Company 1")
    company2 = st.text_input("Company 2")
    role2 = st.text_input("Role at Company 2")
    years2 = st.text_input("Years at Company 2")
    skills = st.text_input("Skills (comma separated)")

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "experience": [
            {"company": company1, "role": role1, "years": years1},
            {"company": company2, "role": role2, "years": years2}
        ],
        "skills": [s.strip() for s in skills.split(",")]
    }

    # Render HTML
    template = Template(template_str)
    html_out = template.render(**user_data)

    # Convert to PDF
    pdf_path = "resume_cloud.pdf"
    convert_html_to_pdf(html_out, pdf_path)

    with open(pdf_path, "rb") as f:
        st.success("✅ Resume generated successfully!")
        st.download_button("📄 Download Your Resume", f, file_name="resume.pdf")

    os.remove(pdf_path)
