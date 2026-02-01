import streamlit as st
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="CV Automation Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
    }
    .delete-button>button {
        background-color: #e74c3c;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'groq_key_saved' not in st.session_state:
        st.session_state.groq_key_saved = False
    if 'education_count' not in st.session_state:
        st.session_state.education_count = 1
    if 'work_ex_count' not in st.session_state:
        st.session_state.work_ex_count = 1
    if 'custom_sections' not in st.session_state:
        st.session_state.custom_sections = []
    if 'skills' not in st.session_state:
        st.session_state.skills = []
    if 'databases' not in st.session_state:
        st.session_state.databases = []
    if 'cloud' not in st.session_state:
        st.session_state.cloud = []
    if 'certifications' not in st.session_state:
        st.session_state.certifications = []
    if 'awards' not in st.session_state:
        st.session_state.awards = []

initialize_session_state()

# Function to save Groq API key to .env file
def save_groq_key_to_env(api_key):
    """
    Save the Groq API key to a .env file
    This is a placeholder function - implement your backend logic here
    """
    try:
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}\n")
        return True
    except Exception as e:
        st.error(f"Error saving API key: {str(e)}")
        return False

# Function to process CV data
def process_cv_data(cv_data):
    """
    Placeholder function to process CV data with backend
    Replace this with your actual backend processing logic
    """
    # Your backend processing logic here
    pass

# Main app
st.markdown('<div class="main-header">📄 CV Automation Tool</div>', unsafe_allow_html=True)

# Sidebar for Groq API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if not st.session_state.groq_key_saved:
        st.info("Please enter your Groq API key to get started")
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your free-tier Groq API key. This will be saved locally."
        )
        
        if st.button("Save API Key", use_container_width=True):
            if groq_api_key:
                if save_groq_key_to_env(groq_api_key):
                    st.session_state.groq_key_saved = True
                    st.success("✅ API Key saved successfully!")
                    st.rerun()
            else:
                st.error("Please enter a valid API key")
    else:
        st.success("✅ API Key configured")
        if st.button("Reset API Key", use_container_width=True):
            st.session_state.groq_key_saved = False
            st.rerun()
    
    st.divider()
    st.markdown("### 📊 Form Progress")
    st.info("Fill out all sections to generate your CV")

# Only show the form if API key is saved
if st.session_state.groq_key_saved:
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Personal Info", 
        "🎓 Education", 
        "💼 Work Experience", 
        "🛠️ Skills & Certifications",
        "➕ Custom Sections"
    ])
    
    # Tab 1: Personal Information
    with tab1:
        st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john.doe@example.com")
            mobile = st.text_input("Mobile Number *", placeholder="+1 234 567 8900")
        
        with col2:
            linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/johndoe")
            github_url = st.text_input("GitHub URL", placeholder="https://github.com/johndoe")
            
        col3, col4 = st.columns(2)
        with col3:
            city = st.text_input("City *", placeholder="New York")
        with col4:
            country = st.text_input("Country *", placeholder="United States")
    
    # Tab 2: Education
    with tab2:
        st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
        
        # Add/Remove education buttons
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("➕ Add Education", use_container_width=True):
                st.session_state.education_count += 1
        with col2:
            if st.session_state.education_count > 1:
                if st.button("➖ Remove Last", use_container_width=True):
                    st.session_state.education_count -= 1
        
        st.divider()
        
        education_data = []
        for i in range(st.session_state.education_count):
            with st.expander(f"Education #{i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    course_name = st.text_input(
                        "Course/Degree Name *",
                        key=f"edu_course_{i}",
                        placeholder="Bachelor of Science in Computer Science"
                    )
                    university_name = st.text_input(
                        "University/Institution Name *",
                        key=f"edu_uni_{i}",
                        placeholder="MIT"
                    )
                    grade = st.text_input(
                        "Grade/GPA",
                        key=f"edu_grade_{i}",
                        placeholder="3.8/4.0"
                    )
                
                with col2:
                    start_year = st.text_input(
                        "Start Year *",
                        key=f"edu_start_{i}",
                        placeholder="2018"
                    )
                    end_year = st.text_input(
                        "End Year *",
                        key=f"edu_end_{i}",
                        placeholder="2022"
                    )
                
                modules = st.text_area(
                    "Key Modules/Courses (comma-separated)",
                    key=f"edu_modules_{i}",
                    placeholder="Data Structures, Algorithms, Machine Learning, Database Systems",
                    help="Enter modules separated by commas"
                )
                
                education_data.append({
                    "course_name": course_name,
                    "university_name": university_name,
                    "start_year": start_year,
                    "end_year": end_year,
                    "modules": [m.strip() for m in modules.split(",") if m.strip()],
                    "grade": grade
                })
    
    # Tab 3: Work Experience
    with tab3:
        st.markdown('<div class="section-header">Work Experience</div>', unsafe_allow_html=True)
        
        # Add/Remove work experience buttons
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("➕ Add Work Experience", use_container_width=True):
                st.session_state.work_ex_count += 1
        with col2:
            if st.session_state.work_ex_count > 1:
                if st.button("➖ Remove Last", use_container_width=True, key="remove_work"):
                    st.session_state.work_ex_count -= 1
        
        st.divider()
        
        work_experience_data = {}
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        
        for i in range(st.session_state.work_ex_count):
            with st.expander(f"Work Experience #{i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    role_name = st.text_input(
                        "Role/Position *",
                        key=f"work_role_{i}",
                        placeholder="Software Engineer"
                    )
                    company = st.text_input(
                        "Company Name *",
                        key=f"work_company_{i}",
                        placeholder="Google"
                    )
                    work_country = st.text_input(
                        "Country *",
                        key=f"work_country_{i}",
                        placeholder="United States"
                    )
                
                with col2:
                    col3, col4 = st.columns(2)
                    with col3:
                        start_month = st.selectbox(
                            "Start Month",
                            months,
                            key=f"work_start_month_{i}"
                        )
                        start_year = st.text_input(
                            "Start Year",
                            key=f"work_start_year_{i}",
                            placeholder="2022"
                        )
                    with col4:
                        end_month = st.selectbox(
                            "End Month",
                            ["Present"] + months,
                            key=f"work_end_month_{i}"
                        )
                        end_year = st.text_input(
                            "End Year",
                            key=f"work_end_year_{i}",
                            placeholder="2024",
                            disabled=(end_month == "Present")
                        )
                
                experience_points = st.text_area(
                    "Key Achievements/Responsibilities (one per line)",
                    key=f"work_points_{i}",
                    placeholder="• Developed scalable microservices handling 1M+ requests/day\n• Led a team of 5 engineers\n• Improved system performance by 40%",
                    height=150,
                    help="Enter each point on a new line"
                )
                
                work_experience_data[f"work_ex_{i+1}"] = {
                    "role_name": role_name,
                    "company": company,
                    "country": work_country,
                    "start_month": start_month,
                    "start_year": start_year,
                    "end_month": end_month if end_month != "Present" else "",
                    "end_year": end_year if end_month != "Present" else "",
                    "experience_points": [point.strip().lstrip("•").strip() 
                                         for point in experience_points.split("\n") 
                                         if point.strip()]
                }
    
    # Tab 4: Skills & Certifications
    with tab4:
        st.markdown('<div class="section-header">Skills & Certifications</div>', unsafe_allow_html=True)
        
        # Skills
        st.subheader("Technical Skills")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            skills_input = st.text_area(
                "Programming Languages/Frameworks",
                placeholder="Python, JavaScript, React, Django",
                help="Enter skills separated by commas"
            )
        
        with col2:
            databases_input = st.text_area(
                "Databases",
                placeholder="PostgreSQL, MongoDB, Redis",
                help="Enter databases separated by commas"
            )
        
        with col3:
            cloud_input = st.text_area(
                "Cloud & DevOps",
                placeholder="AWS, Docker, Kubernetes, CI/CD",
                help="Enter cloud/DevOps tools separated by commas"
            )
        
        st.divider()
        
        # Certifications
        st.subheader("Certifications")
        
        cert_col1, cert_col2 = st.columns([3, 1])
        with cert_col1:
            cert_name = st.text_input("Certification Name", key="cert_name_input")
        with cert_col2:
            cert_link = st.text_input("Credential URL", key="cert_link_input")
        
        if st.button("➕ Add Certification"):
            if cert_name:
                st.session_state.certifications.append({
                    "certification_name": cert_name,
                    "link": cert_link
                })
                st.success(f"Added: {cert_name}")
        
        # Display added certifications
        if st.session_state.certifications:
            st.write("**Added Certifications:**")
            for idx, cert in enumerate(st.session_state.certifications):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{idx+1}. {cert['certification_name']}")
                with col2:
                    if st.button("🗑️", key=f"delete_cert_{idx}"):
                        st.session_state.certifications.pop(idx)
                        st.rerun()
        
        st.divider()
        
        # Awards & Achievements
        st.subheader("Awards & Achievements")
        awards_input = st.text_area(
            "Awards & Achievements (one per line)",
            placeholder="Winner of XYZ Hackathon 2023\nPublished research paper in IEEE\nDean's List for Academic Excellence",
            height=120
        )
    
    # Tab 5: Custom Sections
    with tab5:
        st.markdown('<div class="section-header">Custom Sections</div>', unsafe_allow_html=True)
        st.info("Add custom sections like 'Mentoring Experience', 'Volunteer Work', 'Projects', etc.")
        
        # Add new custom section
        with st.expander("➕ Add New Custom Section", expanded=False):
            section_heading = st.text_input(
                "Section Heading",
                placeholder="e.g., Mentoring Experience, Volunteer Work"
            )
            
            custom_role = st.text_input("Role/Title", placeholder="e.g., Mentor, Volunteer")
            custom_org = st.text_input("Organization/Place", placeholder="e.g., Code Academy")
            custom_location = st.text_input("Location", placeholder="e.g., New York, USA")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_start_date = st.date_input("Start Date", key="custom_start")
            with col2:
                custom_end_date = st.date_input("End Date", key="custom_end")
            
            custom_description = st.text_area(
                "Description/Key Points (one per line)",
                placeholder="• Mentored 20+ students in programming\n• Organized weekly coding workshops",
                height=100
            )
            
            if st.button("Add Custom Section", use_container_width=True):
                if section_heading and custom_role:
                    st.session_state.custom_sections.append({
                        "heading": section_heading,
                        "role_name": custom_role,
                        "organization": custom_org,
                        "location": custom_location,
                        "start_date": str(custom_start_date),
                        "end_date": str(custom_end_date),
                        "description_points": [point.strip().lstrip("•").strip() 
                                              for point in custom_description.split("\n") 
                                              if point.strip()]
                    })
                    st.success(f"✅ Added section: {section_heading}")
                    st.rerun()
                else:
                    st.error("Please fill in at least Section Heading and Role")
        
        st.divider()
        
        # Display custom sections
        if st.session_state.custom_sections:
            st.subheader("Your Custom Sections")
            for idx, section in enumerate(st.session_state.custom_sections):
                with st.expander(f"{section['heading']}", expanded=False):
                    st.write(f"**Role:** {section['role_name']}")
                    st.write(f"**Organization:** {section['organization']}")
                    st.write(f"**Location:** {section['location']}")
                    st.write(f"**Duration:** {section['start_date']} to {section['end_date']}")
                    st.write("**Key Points:**")
                    for point in section['description_points']:
                        st.write(f"• {point}")
                    
                    if st.button(f"🗑️ Delete Section", key=f"delete_custom_{idx}"):
                        st.session_state.custom_sections.pop(idx)
                        st.rerun()
        else:
            st.info("No custom sections added yet")
    
    # Submit button at the bottom
    st.divider()
    st.markdown('<div class="section-header">Generate CV</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate CV", use_container_width=True, type="primary"):
            # Validate required fields
            if not all([name, email, mobile, city, country]):
                st.error("❌ Please fill in all required personal information fields")
            else:
                # Compile all data
                cv_data = {
                    "name": name,
                    "email_id": email,
                    "mobile": mobile,
                    "linkedin_url": linkedin_url,
                    "github_url": github_url,
                    "city": city,
                    "country": country,
                    "education": education_data,
                    "work_experience": work_experience_data,
                    "skills_certifications": {
                        "skills": [s.strip() for s in skills_input.split(",") if s.strip()],
                        "databases": [d.strip() for d in databases_input.split(",") if d.strip()],
                        "cloud": [c.strip() for c in cloud_input.split(",") if c.strip()],
                        "certifications": st.session_state.certifications
                    },
                    "awards_achievements": [a.strip() for a in awards_input.split("\n") if a.strip()],
                    "custom_sections": st.session_state.custom_sections
                }
                
                # Display the compiled data
                with st.expander("📋 View Compiled CV Data (JSON)", expanded=False):
                    st.json(cv_data)
                
                # Process the CV data
                with st.spinner("Processing your CV..."):
                    try:
                        # Call your backend processing function here
                        process_cv_data(cv_data)
                        st.success("✅ CV generated successfully!")
                        
                        # Optionally save to file
                        with open("cv_data.json", "w") as f:
                            json.dump(cv_data, f, indent=4)
                        
                        st.download_button(
                            label="💾 Download CV Data (JSON)",
                            data=json.dumps(cv_data, indent=4),
                            file_name="cv_data.json",
                            mime="application/json"
                        )
                    except Exception as e:
                        st.error(f"❌ Error processing CV: {str(e)}")

else:
    st.warning("⚠️ Please configure your Groq API key in the sidebar to continue")
    st.info("""
    ### How to get your Groq API Key:
    1. Visit [Groq Console](https://console.groq.com)
    2. Sign up for a free account
    3. Navigate to API Keys section
    4. Create a new API key
    5. Copy and paste it in the sidebar
    """)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>CV Automation Tool | Built with Streamlit</p>
        <p style='font-size: 0.8rem;'>Fill out all sections and click 'Generate CV' to create your resume</p>
    </div>
""", unsafe_allow_html=True)