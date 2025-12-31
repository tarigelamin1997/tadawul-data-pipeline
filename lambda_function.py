import json
import os
import requests
import pg8000.native
import boto3  # <--- NEW: AWS SDK to talk to Secrets Manager

# --- CONFIGURATION ---
SECRET_NAME = "tadawul-secrets"
REGION_NAME = "us-east-1"
SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def get_secrets():
    """
    Fetch credentials from AWS Secrets Manager (The Vault).
    """
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=REGION_NAME)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
        # The secret comes back as a JSON string, so we convert it to a Dictionary
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret
    except Exception as e:
        print(f"❌ Failed to fetch secrets: {str(e)}")
        raise e

def get_real_market_data(symbol, api_key):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&apikey={api_key}&outputsize=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "values" not in data:
            print(f"   ⚠️ API Error for {symbol}: {data.get('message', 'Unknown Error')}")
            return None

        latest = data["values"][0]
        return {
            "date": latest["datetime"],
            "open": float(latest["open"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "close": float(latest["close"]),
            "volume": int(latest["volume"])
        }
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        return None

def lambda_handler(event, context):
    print("🚀 Starting US Tech Lambda ETL (v2.0 - Secure Mode)...")
    results = []
    
    try:
        # 1. Open the Vault
        print("🔐 Retrieving secrets from Vault...")
        secrets = get_secrets()
        
        db_host = secrets['DB_HOST']
        db_name = secrets['DB_NAME']
        db_user = secrets['DB_USER']
        db_pass = secrets['DB_PASS']
        api_key = secrets['API_KEY']
        
        # 2. Connect to Database
        conn = pg8000.native.Connection(user=db_user, password=db_pass, host=db_host, database=db_name)
        print("   ✅ Connected to Database")

        # 3. Process Data
        for symbol in SYMBOLS:
            print(f"   📡 Fetching Real Data for {symbol}...")
            data = get_real_market_data(symbol, api_key)
            
            if not data:
                continue

            query = """
                INSERT INTO daily_prices (symbol, date, open, high, low, close, volume)
                VALUES (:symbol, :date, :open, :high, :low, :close, :volume)
                ON CONFLICT (symbol, date) DO NOTHING
            """
            
            conn.run(query, 
                symbol=symbol, 
                date=data['date'], 
                open=data['open'], 
                high=data['high'], 
                low=data['low'], 
                close=data['close'], 
                volume=data['volume']
            )
            results.append(f"{symbol}: Success")

        conn.close()
        return {'statusCode': 200, 'body': json.dumps(results)}

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}