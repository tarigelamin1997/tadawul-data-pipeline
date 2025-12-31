import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

def clean_database():
    try:
        if not DB_PASS:
            print("❌ Error: DB_PASS missing from .env file.")
            return

        print("🧹 Connecting to database...")
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS
        )
        cur = conn.cursor()
        
        # Delete anything ending in .SR (Saudi stocks)
        delete_query = "DELETE FROM daily_prices WHERE symbol LIKE '%.SR';"
        
        cur.execute(delete_query)
        rows_deleted = cur.rowcount
        
        conn.commit()
        print(f"✅ Success! Deleted {rows_deleted} rows containing Saudi data.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clean_database()