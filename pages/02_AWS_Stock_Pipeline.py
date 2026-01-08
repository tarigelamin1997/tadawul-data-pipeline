import streamlit as st
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AWS Data Pipeline",
    page_icon="🏗️",
    layout="wide"
)

# --- HEADER ---
st.title("📈 End-to-End Stock Market Data Pipeline")
st.markdown("### *Automated Cloud Infrastructure for Real-Time Financial Intelligence*")
st.markdown("**Tech Stack:** `AWS` `Terraform` `Airflow` `Python` `DataEngineering`")

st.divider()

# --- EXECUTIVE SUMMARY ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Executive Summary")
    st.markdown(
        """
        **The Business Problem:**
        Tracking market sentiment across thousands of news articles daily is impossible manually. 
        Financial analysts need a way to instantly ingest, process, and visualize stock market news 
        to identify trends without human intervention.

        **The Solution:**
        I architected a fully automated, serverless-first data platform on AWS. 
        Using **Terraform** for Infrastructure as Code, I deployed a secure pipeline that fetches 
        live data via **Apache Airflow**, stores it in an **S3 Data Lake**, and makes it 
        instantly queryable via **Athena** and **QuickSight**.
        """
    )

with col2:
    st.info(
        """
        **🔗 Quick Links**
        - [View Source Code on GitHub](https://github.com/tarigelamin1997/aws-stock-data-pipeline)
        - [Connect on LinkedIn](https://linkedin.com/in/tarigelamin)
        """
    )

st.divider()

# --- ARCHITECTURE ---
st.subheader("🏗️ Architecture & Data Flow")

# Load Image (Make sure the file exists in the 'images' folder!)
try:
    image_arch = Image.open("images/pipeline_architecture.png")
    st.image(image_arch, caption="AWS Serverless Lakehouse Architecture", use_column_width=True)
except FileNotFoundError:
    st.error("⚠️ Image not found. Please upload 'images/pipeline_architecture.png'")

st.markdown(
    """
    **1. Ingestion (Airflow on EC2):** A Python-based DAG fetches raw JSON data from the NewsAPI, handling rate limits automatically.
    
    **2. Storage (S3 Data Lake):** Data is streamed directly to Amazon S3, partitioned by ingestion date.
    
    **3. Cataloging (AWS Glue):** A Glue Crawler inspects the S3 bucket to detect schema changes and update the Data Catalog.
    
    **4. Analysis (AWS Athena):** Serverless SQL queries are run on raw JSON files using `UNNEST` transformations.
    
    **5. Visualization (Amazon QuickSight):** Interactive dashboards track top publishers and keyword trends.
    """
)

st.divider()

# --- ENGINEERING CHALLENGE ---
st.subheader("💡 The Engineering Challenge")
st.markdown(
    """
    **The Challenge: Complex Nested Data**
    The external API returns data in deeply nested JSON arrays. A standard Glue crawler identified the schema 
    but left the data trapped in arrays, making it impossible to visualize directly.

    **The Solution: SQL Transformation**
    I implemented custom SQL transformations in **Athena** using `UNNEST` functions to 'explode' the arrays 
    into flattened analytical rows on the fly.
    """
)

code = '''SELECT 
    article.source.name as source_name,
    article.title,
    article.publishedAt
FROM "portfolio_news_db"."raw_news",
UNNEST(articles) as t(article)'''

st.code(code, language='sql')

st.divider()

# --- RESULTS ---
st.subheader("📸 Project Results")

tab1, tab2 = st.tabs(["📊 Executive Dashboard", "⚙️ Airflow Orchestration"])

with tab1:
    st.markdown("#### Amazon QuickSight Dashboard")
    try:
        image_dash = Image.open("images/quicksight_dashboard.png")
        st.image(image_dash, caption="Real-time analysis of stock news frequency", use_column_width=True)
    except FileNotFoundError:
        st.warning("Upload 'images/quicksight_dashboard.png'")

with tab2:
    st.markdown("#### Apache Airflow DAGs")
    try:
        image_airflow = Image.open("images/airflow_dags.png")
        st.image(image_airflow, caption="Daily scheduled ingestion jobs (Green = Success)", use_column_width=True)
    except FileNotFoundError:
        st.warning("Upload 'images/airflow_dags.png'")