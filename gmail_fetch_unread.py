import imaplib
import email
import os
from email.mime.multipart import MIMEMultipart
from datetime import datetime


import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

GMAIL_APP_PASSSWORD = os.getenv('App_Password')



# Gmail IMAP settings
GMAIL_HOST = 'imap.gmail.com'
GMAIL_PORT = 993



# subject_line = "Security alert"
subject_line = "NCRP MHA Acknowledgement No"
# Your credentials



EMAIL = r"beginasnoob1996@gmail.com"
APP_PASSWORD = GMAIL_APP_PASSSWORD # 16-character app password

def fetch_emails():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL(GMAIL_HOST, GMAIL_PORT)
    mail.login(EMAIL, APP_PASSWORD)
    
    # Select inbox
    mail.select('inbox')
    
    # Search for unread emails only
    status, messages = mail.search(None, 'UNSEEN')
    
    # Get email IDs
    email_ids = messages[0].split()
    
    if not email_ids:
        print("No unread emails found.")
        mail.close()
        mail.logout()
        return
    
    # Create downloads folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    downloads_folder = f'downloads_{timestamp}'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    
    # Fetch unread emails (without marking as read)
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] RFC822.SIZE)')
        
        # Get full message without marking as read
        status, full_msg = mail.fetch(email_id, '(BODY.PEEK[])')
        
        # Parse email
        msg = email.message_from_bytes(full_msg[0][1])
        if subject_line.lower() not in str(msg["Subject"]).lower():
            print("skip")
            continue
        print(f"From: {msg['From']}")
        print(f"Subject: {msg['Subject']}")
        print(f"Date: {msg['Date']}")
        
        # Process attachments
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    # Save attachment
                    filepath = os.path.join(downloads_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded: {filename}")
        
        print("-" * 50)
    
    # Close connection
    mail.close()
    mail.logout()

if __name__ == "__main__":
    fetch_emails()