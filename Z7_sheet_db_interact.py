import gspread
from google.oauth2.service_account import Credentials
import psycopg2
import pandas as pd
import hashlib

# Google Sheets credentials & setup
SHEET_ID = "1u6jPxtNkXM36Sj7DXiso2SxPCrbzqlGQOyqee79YsbU"
SHEET_NAME = "Sheet1"  # change if needed
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "service_account.json"  # path to your service account JSON

# PostgreSQL config
PG_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password"
}

# Connect to Google Sheet
def connect_sheet():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

# Connect to PostgreSQL
def fetch_postgres_data():
    conn = psycopg2.connect(**PG_CONFIG)
    df = pd.read_sql("SELECT * FROM your_table", conn)
    conn.close()
    return df

# Write DataFrame to Sheet
def df_to_sheet(sheet, df):
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Read sheet to DataFrame
def sheet_to_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Detect change via hash
def dataframe_hash(df):
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

# Update PostgreSQL table from DataFrame
def update_postgres(df):
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM your_table")  # Warning: full overwrite
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO your_table (col1, col2, ...) VALUES (%s, %s, ...)", tuple(row))
    conn.commit()
    cursor.close()
    conn.close()

# Main sync logic
def sync():
    sheet = connect_sheet()

    # Step 1: Fetch from PostgreSQL
    pg_df = fetch_postgres_data()
    pg_hash = dataframe_hash(pg_df)

    # Step 2: Fetch from Sheet
    sheet_df = sheet_to_df(sheet)
    sheet_hash = dataframe_hash(sheet_df)

    if pg_hash != sheet_hash:
        print("Mismatch detected. Syncing...")
        if len(sheet_df) == 0:
            # Sheet is empty — upload from DB
            print("Sheet empty, uploading data from database.")
            df_to_sheet(sheet, pg_df)
        else:
            # Sheet has changes — update DB
            print("Sheet modified, updating database.")
            update_postgres(sheet_df)
    else:
        print("No changes detected. All in sync.")

if __name__ == "__main__":
    sync()
