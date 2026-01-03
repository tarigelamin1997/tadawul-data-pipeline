import boto3
import json
import urllib.parse
import psycopg2
import pandas as pd
from aws_secrets import get_secrets

print("🔐 Fetching DB Credentials...")
secrets = get_secrets()
DB_HOST = secrets['DB_HOST']
DB_NAME = secrets['DB_NAME']
DB_USER = secrets['DB_USER']
DB_PASS = secrets['DB_PASS']

s3 = boto3.client('s3')

def load_to_db(symbol, df):
    """Inserts DataFrame into RDS"""
    if df.empty: return

    try:
        conn = psycopg2.connect(
            user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME
        )
        cursor = conn.cursor()

        # --- FIX: Use iterrows() instead of items() ---
        for date_obj, row in df.iterrows():
            # Ensure date is a string (Pandas might parse it to Timestamp)
            date_str = str(date_obj)
            
            insert_query = """
            INSERT INTO daily_prices (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO NOTHING;
            """
            cursor.execute(insert_query, (
                symbol, date_str[:10], # Truncate time
                float(row['Open']), float(row['High']), 
                float(row['Low']), float(row['Close']), 
                int(row['Volume'])
            ))
        
        conn.commit()
        print(f"   ✅ Loaded {symbol} to Database.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"   ❌ Database Error: {e}")
        raise e

def lambda_handler(event, context):
    print("🚀 V2 CODE IS RUNNING (ITERROWS FIX APPLIED)")  # <--- ADD THIS LINE
    print("⚙️ Starting Processor (S3 -> RDS)...")
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    print(f"   📂 Processing file: {key}")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        
        symbol = key.split('/')[-1].replace('.json', '')
        
        df = pd.DataFrame.from_dict(json_content, orient='index')
        
        load_to_db(symbol, df)
        
        return {'statusCode': 200, 'body': json.dumps('Processing Complete')}
        
    except Exception as e:
        print(e)
        raise e