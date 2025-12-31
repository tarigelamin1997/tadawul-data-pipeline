import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

try:
    if not DB_PASS:
        raise ValueError("❌ DB_PASS is missing. Did you create the .env file?")

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    
    # Get last 10 rows
    df = pd.read_sql("SELECT * FROM daily_prices ORDER BY date DESC LIMIT 10", conn)
    
    print("\n📊 DATA CURRENTLY IN DB:")
    print(df)
    
    conn.close()

except Exception as e:
    print(e)