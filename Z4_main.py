# import json
# import psycopg2
# import os
# from Z4_1_db_config import DB_CONFIG
# from datetime import datetime
# import json

# from Z1_gmail_fetch_unread import fetch_emails
# from Z2_remove_password import remove_pdf_password
# from Z3_extract_data1 import process_and_save_json_from_pdf

# def calculate_ageing_days1(date_str):
#     """
#     Calculate ageing in days from a string like '10/10/2024 18:18:PM'.

#     Args:
#         date_str (str): Date string in the format 'DD/MM/YYYY HH:MM:PM'

#     Returns:
#         int: Number of days from date_str to today
#     """
#     try:
#         # Remove :PM or :AM if present (since time is 24-hour)
#         cleaned_str = date_str.replace(":PM", "").replace(":AM", "")
        
#         # Parse the corrected string
#         dt = datetime.strptime(cleaned_str, "%d/%m/%Y %H:%M")
        
#         # Calculate ageing
#         today = datetime.now().date()
#         age = (today - dt.date()).days
#         return age

#     except ValueError as e:
#         print("❌ Invalid format:", e)
#         return None

# # # Example usage
# # date_input = "10/10/2024 18:18:PM"
# # age_days = calculate_ageing_days(date_input)
# # print("📆 Ageing (days):", age_days)




# def calculate_ageing_days(mail_date_str):
#     """
#     Calculate ageing (in days) from mail date to today.

#     Args:
#         mail_date_str (str): Date string like "Tuesday, April 1, 2025 4:56:53 PM GMT"
    
#     Returns:
#         int: Number of days between mail_date and today
#     """
#     try:
#         # Clean and parse the mail date
#         clean_str = mail_date_str.replace(" GMT", "")
#         mail_date = datetime.strptime(clean_str, "%A, %B %d, %Y %I:%M:%S %p").date()
        
#         # Get today's date
#         today = datetime.now().date()
        
#         # Calculate difference in days
#         ageing_days = (today - mail_date).days
#         return ageing_days
    
#     except ValueError as e:
#         print("❌ Invalid date format:", e)
#         return None

# # # Example usage
# # mail_date = "Tuesday, April 1, 2025 4:56:53 PM GMT"
# # age_days = calculate_ageing_days(mail_date)
# # print("📆 Ageing (days):", age_days)





# def extract_month_from_string(date_str):
#     """
#     Extracts full month name and month number from a datetime string.
    
#     Args:
#         date_str (str): The datetime string (e.g., "Tuesday, April 1, 2025 4:56:53 PM GMT")
    
#     Returns:
#         tuple: (full_month_name, month_number)
#     """
#     try:
#         clean_str = date_str.replace(" GMT", "")
#         dt = datetime.strptime(clean_str, "%A, %B %d, %Y %I:%M:%S %p")
#         return dt.strftime("%B"), dt.month
#     except ValueError as e:
#         print("❌ Failed to parse date:", e)
#         return None, None

# # # Example usage
# # date_input = "Tuesday, April 1, 2025 4:56:53 PM GMT"
# # month_name, month_number = extract_month_from_string(date_input)
# # print("📅 Month Name:", month_name)    # April
# # print("📆 Month Number:", month_number)  # 4

# protected_file_path = fetch_emails()
# print(protected_file_path)

# input_pdf = protected_file_path



# folder = os.path.dirname(input_pdf)
# base = os.path.basename(input_pdf)
# decrypted_filename = f"unprotected_{base}"
# output_pdf = os.path.join(folder, decrypted_filename)

# print(output_pdf)
# pdf_password = "Zomato@123"

# unprotected_file_path = remove_pdf_password(input_pdf, output_pdf, pdf_password)

# file_path = unprotected_file_path
# # file_path = r'C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\CYBER_Attachment\20250725_102616_[ENCRYPTED] message_un.pdf'
# # file_path = r'C:\Users\bheem\Desktop\sequelstring_zomato\docs\CYBER CELL\1. Cyber Crime Notice Sample.pdf'

# json_pth = process_and_save_json_from_pdf(file_path)

# # json_path = os.path.join(os.path.dirname(__file__), ".\json_data\cyber_data.json")
# json_path = json_pth
# print(json_pth,"popp")

# # json_path = os.path.join(os.path.dirname(__file__), ".\json_data\cyber_data1.json")
# with open(json_path, "r") as file:
#     records = json.load(file)
# # print(records)
# records1 = records['results'][0]
# line_items = records1['LineItems']
# # print(records1['MailDate'])

# month_name, month_number = extract_month_from_string(records1['MailDate'])
# # age_days = calculate_ageing_days(records1['MailDate'])
# # print("📆 Ageing (days):", age_days)





# # query = """
# # INSERT INTO cyber_fraud_reports (
# #     complaint_date, mail_date, mail_month, amount,
# #     reference_number, police_station_address, account_number, name,
# #     mobile_number, email_id, status, ageing_days, debit_from_bank,
# #     region, utr_number, utr_amount, transaction_datetime, total_fraudulent_amount
# # ) VALUES (
# #     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
# # );
# # """
# query = """
# INSERT INTO cyber_fraud_reports (
#     complaint_date, mail_date, mail_month, amount,
#     reference_number, police_station_address, account_number, name,
#     mobile_number, email_id, ageing_days,
#     region, utr_number, utr_amount, transaction_datetime, total_fraudulent_amount
# ) VALUES (
#     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
# );
# """




# try:
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()

#     for item in line_items:
#         print(item)

#         age_days = calculate_ageing_days1(item["ComplaintDate"])

#         values = (
#             item["ComplaintDate"],
#             records1["MailDate"],
#             month_name,
#             item["Amount"],
#             records1["RefNo"],
#             records1["Police_Station_Address"],
#             item["Account_No"],
#             records1["Name"],
#             records1["Mobile"],
#             records1["Email"],
#             # records1["status"],
#             age_days,
#             # records1["debit_from_bank"],
#             item["Region"],
#             item["Utr_No"],
#             item["Utr_Amount"],
#             item["Transaction_Date"],
#             records1["Total_Fraudulant_Amount"]
#         )
#         cur.execute(query, values)

#     conn.commit()
#     cur.close()
#     conn.close()
#     print("✅ Inserted all records.")

# except Exception as e:
#     print("❌ Error:", e)































# # import os
# # import json
# # # Load JSON data
# # json_path = os.path.join(os.path.dirname(__file__), ".\json_data\cyber_data.json")
# # with open(json_path) as file:
# #     records = json.load(file)
# # # print(records['results'][0])
# # records1 = records['results'][0]
# # line_items = records1['LineItems']
# # # print(records['results'][0]['LineItems'])
# # print(line_items)