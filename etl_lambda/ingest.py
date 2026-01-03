import yfinance as yf
import boto3
import json
import pandas as pd
from datetime import datetime

# S3 Configuration
S3_BUCKET_NAME = "tadawul-data-lake-v1-tarig-elamin"
SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def save_raw_to_s3(data: pd.DataFrame, symbol: str):
    s3 = boto3.client('s3')
    today = datetime.now()
    # Path: raw/YYYY/MM/DD/symbol.json
    path = f"raw/{today.year}/{today.month:02d}/{today.day:02d}/{symbol}.json"
    
    # Save as JSON
    json_data = data.to_json(orient="index", date_format="iso")
    
    try:
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=path,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"   🌊 Saved to S3: {path}")
    except Exception as e:
        print(f"   ⚠️ S3 Upload Failed: {e}")
        raise e

def lambda_handler(event, context):
    print("🚀 Starting Ingest (API -> S3)...")
    
    for symbol in SYMBOLS:
        print(f"   📡 Fetching {symbol}...")
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")
        
        if not data.empty:
            save_raw_to_s3(data, symbol)
        else:
            print(f"   ⚠️ No data for {symbol}")

    return {'statusCode': 200, 'body': json.dumps('Ingest Complete')}