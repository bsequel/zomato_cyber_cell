import os
import json
import psycopg2
from datetime import datetime
from Z4_1_config import DB_CONFIG,PDF_PASSWORD
from Z1_gmail_fetch_unread import fetch_emails
from Z2_remove_password import remove_pdf_password
from Z3_extract_data1 import process_and_save_json_from_pdf
from Z4_report_generate import export_cyber_fraud_data_to_excel

# ────────────────────────────────────────────────────────────────────────
#  Date Processing Utilities
# ────────────────────────────────────────────────────────────────────────

def calculate_ageing_days1(date_str):
    """
    Calculate ageing in days from a date string like '10/10/2024 18:18:PM'.
    """
    try:
        cleaned_str = date_str.replace(":PM", "").replace(":AM", "")
        dt = datetime.strptime(cleaned_str, "%d/%m/%Y %H:%M")
        today = datetime.now().date()
        return (today - dt.date()).days
    except ValueError as e:
        print(" Invalid ComplaintDate format:", e)
        return None


def calculate_ageing_days(mail_date_str):
    """
    Calculate ageing (in days) from mail date string like:
    "Tuesday, April 1, 2025 4:56:53 PM GMT"
    """
    try:
        clean_str = mail_date_str.replace(" GMT", "")
        mail_date = datetime.strptime(clean_str, "%A, %B %d, %Y %I:%M:%S %p").date()
        today = datetime.now().date()
        return (today - mail_date).days
    except ValueError as e:
        print("❌ Invalid MailDate format:", e)
        return None


def extract_month_from_string(date_str):
    """
    Extracts full month name and number from a date string like:
    "Tuesday, April 1, 2025 4:56:53 PM GMT"
    """
    try:
        clean_str = date_str.replace(" GMT", "")
        dt = datetime.strptime(clean_str, "%A, %B %d, %Y %I:%M:%S %p")
        return dt.strftime("%B"), dt.month
    except ValueError as e:
        print("❌ Failed to parse date:", e)
        return None, None


# ────────────────────────────────────────────────────────────────────────
#  Step 1: Fetch and Decrypt Email PDF Attachment
# ────────────────────────────────────────────────────────────────────────

print("Fetching email attachment...")
protected_file_path = fetch_emails()
print("Encrypted PDF:", protected_file_path)

# Decrypt the PDF
# pdf_password = "Zomat"
folder = os.path.dirname(protected_file_path)
base = os.path.basename(protected_file_path)
decrypted_filename = f"unprotected_{base}"
output_pdf = os.path.join(folder, decrypted_filename)

print("Decrypting PDF...")
remove_pdf_password(protected_file_path, output_pdf,PDF_PASSWORD)


# ────────────────────────────────────────────────────────────────────────
#  Step 2: Extract data and save JSON
# ────────────────────────────────────────────────────────────────────────

print("Extracting data from PDF...")
json_path = process_and_save_json_from_pdf(output_pdf)
print(f"JSON saved at: {json_path}")

with open(json_path, "r") as file:
    records = json.load(file)

records1 = records['results'][0]
line_items = records1['LineItems']
month_name, month_number = extract_month_from_string(records1['MailDate'])


# ────────────────────────────────────────────────────────────────────────
#  Step 3: Prepare Insert Query
# ────────────────────────────────────────────────────────────────────────

query = """
INSERT INTO cyber_fraud_reports (
    complaint_date, mail_date, mail_month, amount,
    reference_number, police_station_address, account_number, name,
    mobile_number, email_id, ageing_days,
    region, utr_number, utr_amount, transaction_datetime, total_fraudulent_amount
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""


# ────────────────────────────────────────────────────────────────────────
#    Step 4: Insert into PostgreSQL
# ────────────────────────────────────────────────────────────────────────

try:
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for item in line_items:
        print("Inserting:", item)
        age_days = calculate_ageing_days1(item["ComplaintDate"])

        values = (
            item["ComplaintDate"],
            records1["MailDate"],
            month_name,
            item["Amount"],
            records1["RefNo"],
            records1["Police_Station_Address"],
            item["Account_No"],
            records1["Name"],
            records1["Mobile"],
            records1["Email"],
            age_days,
            item["Region"],
            item["Utr_No"],
            item["Utr_Amount"],
            item["Transaction_Date"],
            records1["Total_Fraudulant_Amount"]
        )

        cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All records inserted successfully.")

except Exception as e:
    print("Database Error:", e)


# ────────────────────────────────────────────────────────────────────────
#    Step 5: REPORT GENERATE IN EXCEL
# ────────────────────────────────────────────────────────────────────────
export_cyber_fraud_data_to_excel()