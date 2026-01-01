import streamlit as st
import pandas as pd
import psycopg2
import boto3
import json
import plotly.express as px
import os
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="US Tech Stocks", page_icon="📈", layout="wide")

# Load environment variables
load_dotenv()

# --- SECURITY: Fetch Credentials ---
def get_db_connection():
    """
    Tries to get creds from AWS Secrets Manager first.
    Falls back to local .env file if AWS fails.
    """
    db_host, db_name, db_user, db_pass = None, None, None, None
    
    # 1. Try AWS Secrets Manager
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name='us-east-1')
        secret_value = client.get_secret_value(SecretId='tadawul-secrets')
        secret = json.loads(secret_value['SecretString'])
        
        db_host = secret['DB_HOST']
        db_name = secret['DB_NAME']
        db_user = secret['DB_USER']
        db_pass = secret['DB_PASS']
        
    except Exception:
        # 2. Fallback to .env (for local testing)
        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASS")

    if not db_pass:
        st.error("❌ Critical Error: No credentials found in AWS Secrets or .env")
        st.stop()

    return psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass
    )

# --- DATA: Query the DB ---
def load_data():
    conn = get_db_connection()
    query = "SELECT * FROM daily_prices ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- UI: The Dashboard Layout ---
st.title("📈 US Tech Stock Tracker")
st.markdown("Automated ETL Pipeline: **AWS Lambda** → **RDS PostgreSQL**")

# Refresh Button
if st.button("🔄 Refresh Data"):
    st.rerun()

# Load Data
try:
    df = load_data()
    
    # Quick Stats Row
    latest_date = df['date'].max()
    st.info(f"📅 Latest Data Point: **{latest_date}**")

    col1, col2, col3 = st.columns(3)
    
    # Metrics
    for i, symbol in enumerate(["TSLA", "NVDA", "AAPL"]):
        stock_data = df[df['symbol'] == symbol]
        if not stock_data.empty:
            latest_close = stock_data.iloc[-1]['close']
            prev_close = stock_data.iloc[-2]['close'] if len(stock_data) > 1 else latest_close
            change = latest_close - prev_close
            pct_change = (change / prev_close) * 100
            
            with [col1, col2, col3][i]:
                st.metric(
                    label=symbol, 
                    value=f"${latest_close:.2f}", 
                    delta=f"{pct_change:.2f}%"
                )

    # 📊 MAIN CHART
    st.subheader("Price History")
    
    # Create interactive Plotly chart
    fig = px.line(
        df, 
        x='date', 
        y='close', 
        color='symbol', 
        markers=True,
        title='Closing Price Trends',
        labels={'close': 'Price (USD)', 'date': 'Date'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Raw Data Table (Collapsible)
    with st.expander("📂 View Raw Database Records"):
        st.dataframe(df.sort_values(by=['date'], ascending=False))

except Exception as e:
    st.error(f"Failed to load data: {e}")