import yfinance as yf
import psycopg2
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Updated to match the US Tech Pivot
SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def extract_data(symbol):
    """EXTRACT: Fetch data from Yahoo Finance"""
    print(f"   📡 Fetching data for {symbol}...")
    stock = yf.Ticker(symbol)
    df = stock.history(period="5d")
    return df

def load_data(symbol, df):
    """LOAD: Insert data into PostgreSQL"""
    if df.empty:
        print(f"   ⚠️ No data found for {symbol}")
        return

    try:
        if not DB_PASS:
            print("   ⚠️  Skipping DB connection: DB_PASS is missing.")
            return

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()

        last_row = df.iloc[-1]
        date = df.index[-1].date()
        
        insert_query = """
        INSERT INTO daily_prices (symbol, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date) DO NOTHING;
        """
        
        cursor.execute(insert_query, (
            symbol, 
            date, 
            float(last_row['Open']), 
            float(last_row['High']), 
            float(last_row['Low']), 
            float(last_row['Close']), 
            int(last_row['Volume'])
        ))
        
        conn.commit()
        print(f"   ✅ Saved {symbol} data for {date} to Database.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"   ❌ Database Error: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🚀 Starting ETL Pipeline (US Tech)...")
    
    for symbol in SYMBOLS:
        data = extract_data(symbol)
        load_data(symbol, data)
        
    print("\n🏁 Pipeline Finished Successfully!")