import streamlit as st
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tarig Elamin | Portfolio",
    page_icon="☁️",
    layout="wide"
)

# --- SIDEBAR INFO ---
with st.sidebar:
    st.image("images/profile.jpg", width=150) # Using your GitHub avatar as placeholder
    st.markdown("### Tarig Elamin")
    st.markdown("Cloud Data Architect & Engineer")
    st.markdown("📍 Riyadh, Saudi Arabia")
    st.markdown("📧 [Email Me](mailto:tarigelamin1997@gmail.com)") # Update with your actual email if needed
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/tarigelamin)")
    st.markdown("🐙 [GitHub](https://github.com/tarigelamin1997)")

# --- MAIN HERO SECTION ---
st.title("Hi, I'm Tarig Elamin 👋")
st.subheader("Building Scalable Cloud Data Platforms on AWS")

st.markdown(
    """
    I am a **Cloud Data Architect & Engineer** specializing in designing secure, automated data pipelines 
    and serverless analytics solutions. My work bridges the gap between raw data and business intelligence 
    using modern cloud-native tools.
    
    **Core Tech Stack:** `AWS` `Python` `Terraform` `Docker` `SQL` `Airflow`
    """
)

st.divider()

# --- THE GALLERY (PROJECTS) ---
st.header("📂 The Gallery")
st.markdown("**👈 Select a project from the sidebar** to see the full case study and live demos.")

col1, col2 = st.columns(2)

# Project 1: US Tech Stock Dashboard
with col1:
    st.info("**1. US Tech Stock Dashboard**")
    st.markdown(
        """
        * **Type:** Live Interactive App
        * **Tech:** AWS Lambda, RDS, Plotly
        * **Summary:** Real-time ETL pipeline visualizing market data for TSLA, NVDA, and AAPL.
        """
    )

# Project 2: AWS Stock Data Pipeline (NEW)
with col2:
    st.success("**2. End-to-End Stock Data Pipeline**")
    st.markdown(
        """
        * **Type:** Enterprise Architecture Case Study
        * **Tech:** Terraform, Airflow, S3, Athena
        * **Summary:** Fully automated data lakehouse architecture handling ingestion, storage, and BI.
        """
    )

st.divider()

# --- CERTIFICATIONS & SKILLS ---
st.subheader("🏆 Certifications")
st.markdown(
    """
    * **AWS Certified Solutions Architect – Associate**
    * **AWS Certified Cloud Practitioner**
    * **Professional Data Engineer** (DataCamp)
    * **IBM Certified Data Analyst**
    """
)

st.markdown("---")
st.caption("© 2026 Tarig Elamin. Built with Python & Streamlit on AWS Elastic Beanstalk.")