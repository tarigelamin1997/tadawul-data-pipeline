import streamlit as st

st.set_page_config(
    page_title="Tarig's Portfolio",
    page_icon="👋",
)

st.write("# Welcome to My Data Engineering Portfolio! 👋")

st.sidebar.success("Select a Project above.")

st.markdown(
    """
    ### Who am I?
    I am a **Data Engineer** specializing in building automated cloud pipelines.
    My goal is to turn raw, messy data into clear, actionable insights using AWS and Python.

    ### 🛠 Tech Stack
    - **Cloud:** AWS (Lambda, RDS, EventBridge, Secrets Manager, Beanstalk)
    - **Code:** Python, SQL, Pandas
    - **DevOps:** Docker, GitHub Actions, Terraform

    ### 📂 The Gallery (Projects)
    **👈 Select a project from the sidebar** to see my live work.
    
    * **Project 1: US Tech Stock ETL Pipeline**
        * Fetches live market data for TSLA, NVDA, AAPL.
        * Automates daily storage into PostgreSQL.
        * Visualizes trends using Plotly.
    """
)