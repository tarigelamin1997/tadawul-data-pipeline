import yfinance as yf
import psycopg2
import pandas as pd
import boto3
import json
from datetime import datetime
from aws_secrets import get_secrets  # Uses your new secure vault

# --- CONFIGURATION (UPDATED for v4 & v5) ---
# Fetch credentials securely from AWS Secrets Manager
print("🔐 Fetching credentials from AWS Secrets Manager...")
secrets = get_secrets()

DB_HOST = secrets['DB_HOST']
DB_NAME = secrets['DB_NAME']
DB_USER = secrets['DB_USER']
DB_PASS = secrets['DB_PASS']

# S3 Configuration for v5.0 Data Lake
S3_BUCKET_NAME = "tadawul-data-lake-v1-tarig-elamin"

SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def save_raw_to_s3(data: pd.DataFrame, symbol: str):
    """
    v5.0: Saves raw data to S3 (Bronze Layer) before processing.
    Path format: raw/YYYY/MM/DD/symbol.json
    """
    s3 = boto3.client('s3')
    
    # Create partitioned path
    today = datetime.now()
    path = f"raw/{today.year}/{today.month:02d}/{today.day:02d}/{symbol}.json"
    
    # Convert DataFrame to JSON string
    # orient='index' creates a structure like {date: {open: 100, close: 101}}
    json_data = data.to_json(orient="index", date_format="iso")
    
    try:
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=path,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"   🌊 Raw data saved to S3 Lake: {path}")
    except Exception as e:
        print(f"   ⚠️ Failed to save to S3: {e}")

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
def lambda_handler(event, context):
    """Standard entry point for AWS Lambda"""
    print("🚀 Starting ETL Pipeline (US Tech)...")
    
    for symbol in SYMBOLS:
        # 1. Extract
        data = extract_data(symbol)
        
        # 2. Archive to S3 (The new v5 step)
        if not data.empty:
            save_raw_to_s3(data, symbol)
        
        # 3. Load to DB
        load_data(symbol, data)
        
    print("\n🏁 Pipeline Finished Successfully!")
    return {
        'statusCode': 200,
        'body': json.dumps('ETL Job Completed')
    }

# For local testing
if __name__ == "__main__":
    lambda_handler(None, None)