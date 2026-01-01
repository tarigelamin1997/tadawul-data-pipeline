import psycopg2
from etl_lambda.aws_secrets import get_secrets

# --- CONFIGURATION ---
print("🔐 Fetching credentials from AWS Secrets Manager...")
secrets = get_secrets()

# Extract values using the EXACT keys from your screenshot
DB_HOST = secrets['DB_HOST']
DB_NAME = secrets['DB_NAME']
DB_USER = secrets['DB_USER']
DB_PASS = secrets['DB_PASS']
# API_KEY = secrets['API_KEY'] # Not used here, but good to have available

def init_database():
    try:
        # Check if password was loaded correctly
        if not DB_PASS:
            print("❌ Error: DB_PASS is missing. Check your AWS Secrets Manager.")
            return

        print("1. Connecting to AWS RDS...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Connected successfully!")

        # SQL to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS daily_prices (
            symbol VARCHAR(20) NOT NULL,
            date DATE NOT NULL,
            open DECIMAL(10, 2),
            high DECIMAL(10, 2),
            low DECIMAL(10, 2),
            close DECIMAL(10, 2),
            volume BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (symbol, date)
        );
        """

        print("2. Creating table 'daily_prices'...")
        cursor.execute(create_table_query)
        print("   ✅ Table created (or already exists)!")

        cursor.close()
        conn.close()
        print("\n🎉 Database is ready for data!")

    except Exception as e:
        print("\n❌ Connection Failed:")
        print(e)
        print("\nTroubleshooting Tip: Check your AWS Security Group and Secrets Manager permissions.")

if __name__ == "__main__":
    init_database()