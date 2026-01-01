import yfinance as yf
import psycopg2
import pandas as pd
import boto3
import json
import os
from datetime import datetime
from aws_secrets import get_secrets

# --- CONFIGURATION ---
print("🔐 Fetching credentials from AWS Secrets Manager...")
secrets = get_secrets()

DB_HOST = secrets['DB_HOST']
DB_NAME = secrets['DB_NAME']
DB_USER = secrets['DB_USER']
DB_PASS = secrets['DB_PASS']
S3_BUCKET_NAME = "tadawul-data-lake-v1-tarig-elamin"
SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def save_raw_to_s3(data: pd.DataFrame, symbol: str):
    """Saves raw data to S3 (Bronze Layer)"""
    s3 = boto3.client('s3')
    today = datetime.now()
    path = f"raw/{today.year}/{today.month:02d}/{today.day:02d}/{symbol}.json"
    
    # Convert to JSON
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

def load_data(symbol, df):
    """Insert data into PostgreSQL"""
    if df.empty: return

    try:
        conn = psycopg2.connect(
            user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME
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
            symbol, date, 
            float(last_row['Open']), float(last_row['High']), 
            float(last_row['Low']), float(last_row['Close']), 
            int(last_row['Volume'])
        ))
        
        conn.commit()
        print(f"   ✅ Saved {symbol} to DB.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"   ❌ Database Error: {e}")

def lambda_handler(event, context):
    print("🚀 Starting ETL Container...")
    
    for symbol in SYMBOLS:
        print(f"   📡 Fetching {symbol}...")
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")
        
        if not data.empty:
            save_raw_to_s3(data, symbol)
            load_data(symbol, data)
        
    return {'statusCode': 200, 'body': json.dumps('Job Complete')}