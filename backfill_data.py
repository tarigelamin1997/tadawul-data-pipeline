import yfinance as yf
import psycopg2
import os
import time
from dotenv import load_dotenv

# Load local .env credentials
load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def backfill_symbol(symbol):
    print(f"⏳ Backfilling last 2 years for {symbol}...")
    
    # 1. Fetch 2 years of data
    stock = yf.Ticker(symbol)
    df = stock.history(period="2y", interval="1d")
    
    if df.empty:
        print(f"❌ No data found for {symbol}")
        return

    # 2. Connect to DB
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        # 3. Insert Loop (Batching would be faster, but this is safer for a simple script)
        count = 0
        for date, row in df.iterrows():
            insert_query = """
                INSERT INTO daily_prices (symbol, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, date) DO NOTHING;
            """
            cursor.execute(insert_query, (
                symbol,
                date.date(),
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close']),
                int(row['Volume'])
            ))
            count += 1
            
        conn.commit()
        print(f"   ✅ Inserted/Checked {count} days of data for {symbol}.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Historical Backfill...")
    
    for symbol in SYMBOLS:
        backfill_symbol(symbol)
        time.sleep(1) # Be nice to the API
        
    print("\n🎉 Backfill Complete! Refresh your dashboard.")