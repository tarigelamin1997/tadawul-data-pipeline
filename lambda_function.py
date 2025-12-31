import json
import os
import requests
import pg8000.native

# --- CONFIGURATION ---
# We use os.environ.get so the code reads from AWS secrets when running there,
# but uses a placeholder when sitting on GitHub.
DB_HOST = os.environ.get("DB_HOST", "tadawul-db.c8xyiyy40mmd.us-east-1.rds.amazonaws.com")
DB_NAME = os.environ.get("DB_NAME", "tadawul")
DB_USER = os.environ.get("DB_USER", "postgres")

# 🔒 SECRET: Never hardcode this in the file you push to GitHub!
DB_PASS = os.environ.get("DB_PASS", "PLACEHOLDER_PASSWORD")

# 🔒 SECRET: Never hardcode this!
API_KEY = os.environ.get("API_KEY", "PLACEHOLDER_API_KEY")

SYMBOLS = ["TSLA", "NVDA", "AAPL"]

def get_real_market_data(symbol):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&apikey={API_KEY}&outputsize=1"
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
    print("🚀 Starting US Tech Lambda ETL...")
    results = []
    
    conn = None
    try:
        conn = pg8000.native.Connection(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
        print("   ✅ Connected to Database")

        for symbol in SYMBOLS:
            print(f"   📡 Fetching Real Data for {symbol}...")
            data = get_real_market_data(symbol)
            
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
        print(f"❌ Database Error: {str(e)}")
        if conn: conn.close()
        return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}