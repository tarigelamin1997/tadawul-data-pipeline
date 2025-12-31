import psycopg2
import pandas as pd
import os

# --- CONFIGURATION ---
# Uses environment variables if available, otherwise uses placeholders for safety
DB_HOST = os.environ.get("DB_HOST", "tadawul-db.c8xyiyy40mmd.us-east-1.rds.amazonaws.com")
DB_NAME = os.environ.get("DB_NAME", "tadawul")
DB_USER = os.environ.get("DB_USER", "postgres")

# 🔒 SAFE: No real password here
DB_PASS = os.environ.get("DB_PASS", "PLACEHOLDER_PASS")

try:
    if DB_PASS == "PLACEHOLDER_PASS":
        print("⚠️  Warning: You are using a placeholder password. Set DB_PASS environment variable to run.")
    
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    
    # Simple SQL query to get everything
    df = pd.read_sql("SELECT * FROM daily_prices ORDER BY date DESC", conn)
    
    print("\n📊 DATA CURRENTLY IN DB:")
    print(df)
    
    conn.close()

except Exception as e:
    print(e)